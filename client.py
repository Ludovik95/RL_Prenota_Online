from datetime import datetime
import json
import logging
from typing import Optional
from curl_cffi import requests

from objects import Patient, Prescription, Appointment

class Client:

    def __init__(self, debug: bool = False):

        self._debug_conf(debug)

        self.session = requests.Session(headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en,it;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "DNT": "1",
            "Host": "prenotasalute.regione.lombardia.it",
            "Origin": "https://prenotasalute.regione.lombardia.it",
            "Priority": "u=0",
            "Referer": "https://prenotasalute.regione.lombardia.it/prenotaonline/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
            "X-Prenota-Online-Channel": "WEB",
            "X-Prenota-Online-Info": "04.20.21|linux|unknown|firefox 140.0",
        })

        # Initialize session by making a GET request
        self.url = "https://prenotasalute.regione.lombardia.it/prenotaonline/jsonBroker"
        self.session.get(self.url, verify=False)
        self._get_token()
        self._get_province_codes()


    def login(
        self,
        codice_fiscale: str,
        codice_tessera: str) -> Optional[Patient]:

        result = self._send_request(
            self._generate_request_data(
                destination = "pgpcitt_login_gp_prv",
                arguments = {
                    "codiceFiscale": codice_fiscale,
                    "crs": codice_tessera,
                    "dataScadenza": "",
                    "flagIncludiCrsNonAttive": "N"
                }
            )
        )

        self.session.headers["X-Prenota-Online-Token"] += " | {} | {}".format(codice_fiscale, codice_tessera)

        patient_data = result.get("cittadino")
        if patient_data:
            patient = Patient.from_dict(patient_data)
            logging.debug(f"Logged in successfully for patient: {patient.nome} {patient.cognome}")
            return patient
        else:
            logging.error("Failed to retrieve patient data after login.")


    def get_appointment(
        self,
        codice_fiscale: str,
        id_ricetta: str) -> Optional[Appointment]:

        result = self._send_request(
            self._generate_request_data(
                destination = "pgpcitt_ricerca_appuntamento",
                arguments = {
                    "codiceFiscale": codice_fiscale,
                    "tipo": "6",
                    "iup": None,
                    "iurp": None,
                    "nre": id_ricetta,
                    "rur": None,
                    "ipCup": None,
                    "periodo": { "dal": "20000101000000", "al": None }
                }
            )
        )

        appointment_list = result.get("appuntamenti").get("singoli")
        if appointment_list:
            appointment = Appointment.from_dict(appointment_list[0])
            return appointment

        return None


    def get_prescription(
        self,
        codice_fiscale: str,
        id_ricetta: str) -> Optional[Prescription]:

        result = self._send_request(
            self._generate_request_data(
                destination = "pgpcitt_ricerca_ricetta",
                arguments = {
                    "codiceFiscale": codice_fiscale,
                    "iup": None,
                    "iurp": None,
                    "nre": id_ricetta,
                    "rur": None,
                    "periodo": { "dal": None, "al": None },
                    "flagFlussoPostoInCoda": "N",
                    "flagIncludiNonPrenotabili": "N",
                    "codicePrestazione": "",
                    "categoriaPrestazione": ""
                }
            )
        )

        if result:
            ricetta = result.get("ricette")[0]
            prescription = Prescription.from_dict(ricetta) if ricetta else None
            return prescription
        
        return None


    def check_prescription(
        self):

        logging.debug("step 04 - check prescription")


    def get_payment(
        self,
        appointment: Appointment) -> Optional[dict]:

        result = self._send_request(
            self._generate_request_data(
                destination = "pgpcitt_ricerca_pagamento",
                arguments = {
                    "codiceFiscale": appointment.cittadino["codice_fiscale"],
                    "iup": appointment.iup,
                    "iurp": appointment.iurp
                }
            )
        )

        return result


    def get_availability(
        self,
        patient: Patient,
        prescription: Prescription,
        provincia: str) -> list[dict]:

        for prov in self.province_data:
            if prov.get("descrizione") == provincia.upper():
                zona = prov
                zona["codice"] = zona.get("codiceProvincia") + zona.get("codiceComune")
                break

        today = datetime.now().strftime("%Y%m%d") + "000000"

        result = self._send_request(
            self._generate_request_data(
                destination = "pgpcitt_ricerca_disponibilita",
                arguments = {
                    "codiceFiscale": patient.codiceFiscale,
                    "zona": zona,
                    "ricetta": prescription.__dict__,
                    "tipoPrestazione": "Z",
                    "presidi": [],
                    "aziende": [],
                    "recapiti": {
                        "telefono": patient.telefono,
                        "cellulare": patient.cellulare,
                        "email": patient.email
                    },
                    "vincoliTemporali": {
                        "dal": today,
                        "al": None,
                        "lunedi": "S",
                        "martedi": "S",
                        "mercoledi": "S",
                        "giovedi": "S",
                        "venerdi": "S",
                        "sabato": "S",
                        "domenica": "S",
                        "mattina": "S",
                        "pomeriggio": "S"
                    },
                    "caricaRequestRicercaAgende": "N",
                    "minDal": None,
                    "ats": None,
                    "tipoNegoziazione": None,
                    "regimeErogazione": None,
                    "risorsa": None,
                    "codiceProvincia": None,
                    "codiceComune": None,
                    "codiceStruttura": None
                }
            )
        )

        return result.get("singole")


    def _get_token(self):
        result = self._send_request(
            self._generate_request_data(
                destination = "pgpcitt_genera_token",
                arguments = {}
            )
        )

        self.session.headers["X-Prenota-Online-Token"] = result


    def _get_province_codes(self):
        province_data = self._send_request(
            self._generate_request_data(
                destination = "pgpcitt_ricerca_zona",
                arguments = {}
            )
        )

        self.province_data = province_data

        '''
        province_data = [
            {"descrizione":"BERGAMO","codiceProvincia":"016","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"BRESCIA","codiceProvincia":"017","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"COMO","codiceProvincia":"013","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"CREMONA","codiceProvincia":"019","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"LECCO","codiceProvincia":"097","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"LODI","codiceProvincia":"098","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"MANTOVA","codiceProvincia":"020","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"MILANO CITTA'","codiceProvincia":"015","codiceComune":"146","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"MILANO PROVINCIA","codiceProvincia":"015","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"MONZA E DELLA BRIANZA","codiceProvincia":"108","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"PAVIA","codiceProvincia":"018","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"SONDRIO","codiceProvincia":"014","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"},
            {"descrizione":"VARESE","codiceProvincia":"012","codiceComune":"%","abilitazionePiuPiu":"S","abilitazioneNre":"N"}
        ]
        '''

    def _generate_request_data(self, destination: str, arguments: dict):
        data = {
              "metadata": json.dumps(
                {
                    "destination": destination,
                    "method": "handle",
                    "argumentTypes": ["java.lang.String"]
                },
                separators=(",", ":"),
            ),
          "jsonBusinessArg0": json.dumps(arguments, separators=(",", ":"))
        }
        
        return data


    def _send_request(self, data):
        response = self.session.post(
            self.url,
            data=data,
            verify=False
        )

        payload = response.json()

        result = payload.get("result")
        if isinstance(result, str) and result.startswith(("{", "[")):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                logging.error("Failed to decode JSON from result: %s", result)

        warning = payload.get("warning")
        error = payload.get("error")
        exception = payload.get("exception")

        logging.debug("Request data: %s", data)
        logging.debug("Response status code: %d", response.status_code)
        logging.debug("Result: %s", result) if result else logging.debug("Response JSON: %s", response.json())
        logging.debug("Warning: %s", warning) if warning else None
        logging.debug("Error: %s", error) if error else None
        logging.debug("Exception: %s", exception) if exception else None
        logging.debug("----------------------------------------")

        return result


    def _debug_conf(self, debug: bool):

        logging.basicConfig(
            filename=".tests/app.log",
            encoding="utf-8",
            filemode="a",
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
            level=logging.DEBUG if debug else logging.INFO
        )
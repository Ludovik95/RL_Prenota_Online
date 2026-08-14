import json
import logging
from curl_cffi import requests

from objects import Patient, Prescription

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


	def login(
        self,
        codice_fiscale: str,
        codice_tessera: str):

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
			patient = Patient(codice_fiscale, codice_tessera)
			patient.cognome = patient_data.get("cognome")
			patient.nome = patient_data.get("nome")
			patient.sesso = patient_data.get("sesso")
			patient.nascita = patient_data.get("nascita")
			patient.recapiti["telefono"] = patient_data.get("recapiti", {}).get("telefono")
			patient.recapiti["cellulare"] = patient_data.get("recapiti", {}).get("cellulare")
			patient.recapiti["email"] = patient_data.get("recapiti", {}).get("email")
			logging.debug(f"Logged in successfully for patient: {patient.nome} {patient.cognome}")
			return patient
		else:
			logging.error("Failed to retrieve patient data after login.")

		return patient


	def get_appointment(
        self,
        codice_fiscale: str,
        id_ricetta: str):

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

		return result


	def get_prescription(
        self,
        codice_fiscale: str,
        id_ricetta: str):

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

		return result


	def check_prescription(
        self):

		logging.debug("step 04 - check prescription")


	def get_payment(
		self,
		codice_fiscale: str,
		iup: str,
		iurp: str):

		result = self._send_request(
			self._generate_request_data(
				destination = "pgpcitt_ricerca_pagamento",
				arguments = {
					"codiceFiscale": codice_fiscale,
					"iup": iup,
					"iurp": iurp
				}
			)
		)

		return result


	def get_availability(
        self,
        codice_fiscale: str,
        prescription: Prescription,
		provincia: str):

		result = self._send_request(
			self._generate_request_data(
				destination = "pgpcitt_ricerca_disponibilita",
				arguments = {
					"codiceFiscale": codice_fiscale,
					"zona": {
						"descrizione": None,
						"codiceProvincia": None,
						"codiceComune": None,
						"codice": None,
						"abilitazionePiuPiu": None,
						"abilitazioneNre": None
					},
					"ricetta": {
						**prescription.__dict__,
					    "appuntamentiUnificati": None,
					    "daSbloccare": False
					    },
					"tipoPrestazione": None,
					"presidi": [],
					"aziende": [],
					"recapiti": {
						"telefono": None,
						"cellulare": None,
						"email": None
					},
					"vincoliTemporali": {
						"dal": None,
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

		return result


	def _get_token(self):
		result = self._send_request(
			self._generate_request_data(
				destination = "pgpcitt_genera_token",
				arguments = {}
			)
		)

		self.session.headers["X-Prenota-Online-Token"] = result


	def _get_province_code(self, province_name: str):
		result = self._send_request(
			self._generate_request_data(
				destination = "pgpcitt_ricerca_zona",
				arguments = {}
			)
		)
		
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
		for province in province_data:
			if province["descrizione"] == province_name:
				return province["codiceProvincia"]
		return None


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
		if isinstance(result, str) and result.startswith("{"):
			try:
				result = json.loads(result)
			except json.JSONDecodeError:
				logging.error("Failed to decode JSON from result: %s", result)

		warning = payload.get("warning")
		error = payload.get("error")
		exception = payload.get("exception")

		logging.debug(response.status_code)
		logging.debug(result) if result else logging.debug(response.json())
		logging.debug(warning) if warning else None
		logging.debug(error) if error else None
		logging.debug(exception) if exception else None

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
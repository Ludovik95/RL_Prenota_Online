import json
from curl_cffi import requests

class Client:

	def __init__(self):

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

		self.session.headers["X-Prenota-Online-Token"] += " | {} | {}".format(codice_fiscale, codice_tessera)

		response = self._send_request(
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

		return response


	def get_appointment(
        self,
        codice_fiscale: str,
        id_ricetta: str):

		response = self._send_request(
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

		return response


	def get_prescription(
        self,
        codice_fiscale: str,
        id_ricetta: str):

		response = self._send_request(
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

		return response


	def check_prescription(
        self):

		print("step 04 - check prescription")


	def get_availability(
        self,
        codice_fiscale: str,
        id_ricetta: str):

		response = self._send_request(
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

		return response


	def _get_token(self):
		response = self._send_request(
			self._generate_request_data(
				destination = "pgpcitt_genera_token",
				arguments = {}
			)
		)

		if response.status_code == 200:
			try:
				data = response.json()
				if "result" in data:
					self.token = data["result"]
					self.session.headers["X-Prenota-Online-Token"] = self.token
			except json.JSONDecodeError:
				print("Failed to decode JSON response.")


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

		print(data, "\n")
		print(response.status_code, "\n")
		print(response.text, "\n")

		return response
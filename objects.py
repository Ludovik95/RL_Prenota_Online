from dataclasses import dataclass
@dataclass
class Patient:

    def __init__(
            self,
            codice_fiscale: str,
            codice_tessera: str):
        
        self.codice_fiscale = codice_fiscale
        self.codice_tessera = codice_tessera
        self.cognome = None
        self.nome = None
        self.sesso = None
        self.nascita = None
        self.recapiti = {
          "telefono": None,
          "cellulare": None,
          "email": None
        }

@dataclass
class Prescription:

	def __init__(
			self,
			codice_fiscale: str,
			id_ricetta: str
			):
		
		self.datiRispostaMEF = None
		self.data = None
		self.iup = None
		self.iurp = None
		self.cittadino = {
            "codiceFiscale": codice_fiscale
        }
		self.emessaIl = None
		self.scadenzaIl = None
		self.tipo = None
		self.modulo = { 
            "id": id_ricetta,
            "tipo": None
        }
		self.flagRe = None
		self.priorita = None
		self.urgenza = None
		self.tipoPrestazione = None
		self.stato = {
            "codice": None,
            "descrizione": None,
            "data": None
        }
		self.quesitoDiagnostico = {
            "codice": None,
            "descrizione": None,
            "id": None,
            "operatoreLogico": None
        }
		self.note = None
		self.esenzione = {
            "cdNazionale": None,
            "cdStampato": None,
            "codice": None,
            "descrizione": None
        }
		self.flagEsenzionePatologia = None
		self.flagAltreEsenzioni = None
		self.flagSuggerita = None
		self.brancaSpecialistica = None
		self.provenienzaPrescrizione = None
		self.prescrittore = {
            "codiceFiscale": None,
            "codiceRegionale": None,
            "nome": None,
            "cognome": None
        }
		self.nrPrestazioni = None
		self.prestazioni = []
		self.appuntamenti = {
            "singoli": [],
            "combinati": [],
            "associati": [],
            "rpDifferite": []
        }

@dataclass
class Appointment:

    def __init__(
            self,
            uuid: str,
            idAppuntamento: str,
            iup: str,
            iurp: str,
            ipCup: str,
            azienda: dict,
            data: str,
            prestazione: dict,
            differita: bool,
            modulo: str,
            associazione: str,
            cittadino: dict,
            prenotatoIl: str,
            registratoIl: str,
            modificatoIl: str,
            annullatoIl: str,
            noteAnnullamento: str,
            stato: str,
            tipo: str,
            unitaErogante: dict,
            unitaErogatrice: dict,
            agenda: dict,
            infoNote: dict,
            infoNotePreparazione: dict,
            indoLuogoPresentazione: dict,
            infoMemorandum: dict,
            infoNoteDisdettaPrenotazione: dict,
            infoConsensoInformato: dict,
            infoMezzi: dict,
            cicli: list,
            quesitoDiagnostico: dict,
            regimeErogazione: str,
            risorsa: str,
            tariffaLp: str):
        
        self.uuid = uuid
        self.idAppuntamento = idAppuntamento
        self.iup = iup
        self.iurp = iurp
        self.ipCup = ipCup
        self.azienda = azienda
        self.data = data
        self.prestazione = prestazione
        self.differita = differita
        self.modulo = modulo
        self.associazione = associazione
        self.cittadino = cittadino
        self.prenotatoIl = prenotatoIl
        self.registratoIl = registratoIl
        self.modificatoIl = modificatoIl
        self.annullatoIl = annullatoIl
        self.noteAnnullamento = noteAnnullamento
        self.stato = stato
        self.tipo = tipo
        self.unitaErogante = unitaErogante
        self.unitaErogatrice = unitaErogatrice
        self.agenda = agenda
        self.infoNote = infoNote
        self.infoNotePreparazione = infoNotePreparazione
        self.indoLuogoPresentazione = indoLuogoPresentazione
        self.infoMemorandum = infoMemorandum
        self.infoNoteDisdettaPrenotazione = infoNoteDisdettaPrenotazione
        self.infoConsensoInformato = infoConsensoInformato
        self.infoMezzi = infoMezzi
        self.cicli = cicli
        self.quesitoDiagnostico = quesitoDiagnostico
        self.regimeErogazione = regimeErogazione
        self.risorsa = risorsa
        self.tariffaLp = tariffaLp
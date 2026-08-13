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

class Prescription:

	def __init__(
			self,
			datiRispostaMEF: str,
			data: str,
			iup: str,
			iurp: str,
			cittadino: dict,
			emessaIl: str,
			scadenzaIl: str,
			tipo: str,
			modulo: dict,
			flagRe:str,
			priorita: str,
			urgenza: str,
			tipoPrestazione: str,
			stato: dict,
			quesitoDiagnostico: dict,
			note: str,
			esenzione: dict,
			flagEsenzionePatologia: str,
			flagAltreEsenzioni: str,
			flagSuggerita: str,
			brancaSpecialistica: str,
			provenienzaPrescrizione: str,
			prescrittore: dict,
			nrPrestazioni: int,
			prestazioni: list,
			appuntamenti: dict
			):
		
		self.datiRispostaMEF = datiRispostaMEF
		self.data = data
		self.iup = iup
		self.iurp = iurp
		self.cittadino = cittadino
		self.emessaIl = emessaIl
		self.scadenzaIl = scadenzaIl
		self.tipo = tipo
		self.modulo = modulo
		self.flagRe = flagRe
		self.priorita = priorita
		self.urgenza = urgenza
		self.tipoPrestazione = tipoPrestazione
		self.stato = stato
		self.quesitoDiagnostico = quesitoDiagnostico
		self.note = note
		self.esenzione = esenzione
		self.flagEsenzionePatologia = flagEsenzionePatologia
		self.flagAltreEsenzioni = flagAltreEsenzioni
		self.flagSuggerita = flagSuggerita
		self.brancaSpecialistica = brancaSpecialistica
		self.provenienzaPrescrizione = provenienzaPrescrizione
		self.prescrittore = prescrittore
		self.nrPrestazioni = nrPrestazioni
		self.prestazioni = prestazioni
		self.appuntamenti = appuntamenti

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
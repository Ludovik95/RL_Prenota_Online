from dataclasses import dataclass, field, fields, MISSING
from datetime import datetime
from typing import Optional
@dataclass
class Patient:
    codiceFiscale: str
    codice_tessera: Optional[str] = None
    cognome: Optional[str] = None
    nome: Optional[str] = None
    sesso: Optional[str] = None
    nascita: Optional[str] = None
    telefono: Optional[str] = None
    cellulare: Optional[str] = None
    email: Optional[str] = None

    def __init__(
            self,
            codiceFiscale: str,
            codice_tessera: str):
        
        self.codiceFiscale = codiceFiscale
        self.codice_tessera = codice_tessera
    
    @classmethod
    def from_dict(cls, data: dict) -> Optional["Patient"]:
        required_keys = {
            f.name for f in fields(cls) if f.default is MISSING and f.default_factory is MISSING
        }

        if not required_keys.issubset(data.keys()):
            raise ValueError(f"Missing required keys: {required_keys - set(data.keys())}")

        # Create instance without calling __init__
        obj = cls.__new__(cls)
        
        for f in fields(cls):
            if f.name in data and data[f.name] is not None:
                setattr(obj, f.name, data[f.name])
            elif f.default is not MISSING:
                setattr(obj, f.name, f.default)
            elif f.default_factory is not MISSING:
                setattr(obj, f.name, f.default_factory())
        
        return obj


@dataclass
class Prescription:

    cittadino: dict = field(default_factory=lambda: {"codiceFiscale": None})
    modulo: dict = field(default_factory=lambda: { 
        "id": None,
        "tipo": None
    })
    datiRispostaMEF: Optional[str] = None
    data: Optional[str] = None
    iup: Optional[str] = None
    iurp: Optional[str] = None
    emessaIl: Optional[str] = None
    scadenzaIl: Optional[str] = None
    tipo: Optional[str] = None
    flagRe: Optional[str] = None
    priorita: Optional[str] = None
    urgenza: Optional[str] = None
    tipoPrestazione: Optional[str] = None
    stato: Optional[dict] = field(default_factory=lambda: {
        "codice": None,
        "descrizione": None,
        "data": None
        })
    quesitoDiagnostico: Optional[dict] = field(default_factory=lambda: {
        "codice": None,
        "descrizione": None,
        "id": None,
        "operatoreLogico": None
        })
    note: Optional[str] = None
    esenzione: Optional[dict] = field(default_factory=lambda: {
        "cdNazionale": None,
        "cdStampato": None,
        "codice": None,
        "descrizione": None
    })
    flagEsenzionePatologia: Optional[str] = None
    flagAltreEsenzioni: Optional[str] = None
    flagSuggerita: Optional[str] = None
    brancaSpecialistica: Optional[str] = None
    provenienzaPrescrizione: Optional[str] = None
    prescrittore: Optional[dict] = field(default_factory=lambda: {
        "codiceFiscale": None,
        "codiceRegionale": None,
        "nome": None,
        "cognome": None
    })
    nrPrestazioni: Optional[str] = None
    prestazioni: Optional[list] = field(default_factory=list)
    appuntamenti: Optional[dict] = field(default_factory=lambda: {
        "singoli": [],
        "combinati": [],
        "associati": [],
        "rpDifferite": []
    }),
    appuntamentiUnificati: Optional[str] = None
    daSbloccare: Optional[bool] = False

    def __init__(
            self,
            codiceFiscale: str,
            id_ricetta: str
            ):
        
        self.cittadino = {"codiceFiscale": codiceFiscale}
        self.modulo = { 
            "id": id_ricetta,
            "tipo": None
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Prescription"]:
        required_keys = {
            f.name for f in fields(cls) if f.default is MISSING and f.default_factory is MISSING
        }

        if not required_keys.issubset(data.keys()):
            raise ValueError(f"Missing required keys: {required_keys - set(data.keys())}")

        # Create instance without calling __init__
        obj = cls.__new__(cls)
        
        for f in fields(cls):
            if f.name in data and data[f.name] is not None:
                setattr(obj, f.name, data[f.name])
            elif f.default is not MISSING:
                setattr(obj, f.name, f.default)
            elif f.default_factory is not MISSING:
                setattr(obj, f.name, f.default_factory())
        
        return obj


@dataclass
class Appointment:

    uuid: str = None
    idAppuntamento: str = None
    iup: str = None
    iurp: str = None
    modulo: str = None
    associazione: str = None
    ipCup: str = None
    data: str = None
    cittadino: dict = field(default_factory=lambda: {
        "codiceFiscale": None,
        "codiceSanitario": None,
        "nome": None,
        "cognome": None,
        "sesso": None,
        "nascita": None,
        "localita": None,
        "residenza": None,
        "indirizzo": None,
        "tel": None,
        "sms": None,
        "email": None
    })
    azienda: dict = field(default_factory=lambda: {
        "id": None,
        "codice": None,
        "descrizione": None,
        "area": None,
        "email": None,
        "sito": None,
        "flag": {
            "prioritaB": None,
            "differita": None,
            "unitaPrenotante": None,
            "differitaVisibile": None,
            "abilitataPagamento": None
        },
        "infoPrenotazione": {
            "telefono": None,
            "orari": None
        }
    })
    prestazione: dict = field(default_factory=lambda: {
        "codice": None,
        "descrizione": None,
        "codiceDistretto": None,
        "codiceMetodica": None,
        "flagExAsl": None,
        "flagEsameLaboratorio": None,
        "flagAmbulatoriale": None,
        "flagVaccinoAntinfluenzale": None,
        "flagTamponeRapido": None,
        "flagTamponeCovid": None,
        "codiceNomenclatoreNazionale": None,
        "codiceNomenclatoreRegionale": None,
        "codCatalogoPrescr": None
    })
    differita: bool = None
    ricetta: dict = field(default_factory=lambda: {
        "iup": None,
        "iurp": None,
        "cittadino": None,
        "emessaIl": None,
        "scadenzaIl": None,
        "tipo": None,
        "modulo": { "id": None, "tipo": None },
        "flagRe": None,
        "priorita": None,
        "urgenza": None,
        "tipoPrestazione": None,
        "stato": None,
        "quesitoDiagnostico": None,
        "note": None,
        "esenzione": None,
        "flagEsenzionePatologia": None,
        "flagAltreEsenzioni": None,
        "flagSuggerita": None,
        "brancaSpecialistica": None,
        "provenienzaPrescrizione": None,
        "prescrittore": None,
        "nrPrestazioni": None,
        "prestazioni": [],
        "prestazioniPrenotate": [],
        "datiRispostaMEF": None,
        "appuntamenti": None,
        "appuntamentiUnificati": [],
        "daSbloccare": False
    })
    prenotatoIl: str = None
    registratoIl: str = None
    modificatoIl: str = None
    annullatoIl: str = None
    noteAnnullamento: str = None
    stato: str = None
    tipo: str = None
    unitaErogante: dict = field(default_factory=lambda: {
        "codice": None,
        "descrizione": None,
        "telefono": None,
        "puntoIndirizzo": { "localita": None, "indirizzo": None },
        "unitaPrenotante": {
          "codice": None,
          "descrizione": None,
          "azienda": {
            "id": None,
            "codice": None,
            "descrizione": None,
            "area": None,
            "email": None,
            "sito": None,
            "flag": None,
            "infoPrenotazione": None
          },
          "flag": { "inibizioneNre": None }
        },
        "presidio": {
          "id": None,
          "codice": None,
          "descrizione": None,
          "descrizioneEstesa": None,
          "email": None,
          "puntoIndirizzo": {
            "localita": {
              "codice": None,
              "descrizione": None,
              "cap": None,
              "siglaProvincia": None
            },
            "indirizzo": {
              "toponimo": None,
              "descrizione": None,
              "civico": None,
              "frazione": None,
              "coordinate": {
                "latitude": None,
                "longitude": None
              }
            }
          },
          "azienda": {
            "id": None,
            "codice": None,
            "descrizione": None,
            "area": None,
            "email": None,
            "sito": None,
            "flag": {
              "prioritaB": None,
              "differita": None,
              "unitaPrenotante": None,
              "differitaVisibile": None,
              "abilitataPagamento": None
            },
            "infoPrenotazione": { "telefono": None, "orari": [] }
          },
          "telefono": None,
          "orariApertura": None,
          "periodoChiusura": None,
          "distanza": None
        },
        "cdSissUe": None
        })
    unitaErogatrice: dict = field(default_factory=None)
    agenda: dict = field(default_factory=lambda: {
        "codice": None,
        "descrizione": None,
        "note": None,
        "noteAggiuntive": None
    })
    infoNote: dict = field(default_factory=lambda: {
        "testo": None,
        "link": None
    })
    infoNotePreparazione: dict = field(default_factory=lambda: {
        "testo": None,
        "link": None
    })
    infoLuogoPresentazione: dict = field(default_factory=lambda: {
        "testo": None,
        "link": None
    })
    infoMemorandum: dict = field(default_factory=lambda: {
        "testo": None,
        "link": None
    })
    infoNoteDisdettaPrenotazione: dict = field(default_factory=lambda: {
        "testo": None,
        "link": None
    })
    infoConsensoInformato: dict = field(default_factory=lambda: {
        "testo": None,
        "link": None
    })
    infoMezzi: dict = field(default_factory=lambda: {
        "testo": None,
        "link": None
    })
    cicli: list = field(default_factory=[])
    quesitoDiagnostico: dict = field(default_factory=lambda: {
        "codice": None,
        "descrizione": None
    })
    regimeErogazione: str = None
    risorsa: dict = field(default_factory=lambda: {
        "codice": "",
        "descrizione": "",
        "nome": "",
        "cognome": "",
        "azienda": None,
        "idPresidio": None,
        "idAgenda": "",
        "agende": [],
        "aziende": [],
        "presidi": []
    })
    tariffaLp: str = None

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Appointment"]:
        required_keys = {
            f.name for f in fields(cls) if f.default is MISSING and f.default_factory is MISSING
        }

        if not required_keys.issubset(data.keys()):
            raise ValueError(f"Missing required keys: {required_keys - set(data.keys())}")

        # Create instance without calling __init__
        obj = cls.__new__(cls)
        
        # Initialize all fields from data
        for f in fields(cls):
            if f.name in data and data[f.name] is not None:
                setattr(obj, f.name, data[f.name])
            elif f.default is not MISSING:
                setattr(obj, f.name, f.default)
            elif f.default_factory is not MISSING:
                setattr(obj, f.name, f.default_factory())
        
        return obj

    def get_data(self):
        if self.data:
            return datetime.strptime(self.data, "%Y%m%d%H%M%S")
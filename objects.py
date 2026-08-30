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

    uuid: str
    idAppuntamento: str
    iup: str
    iurp: str
    ipCup: str
    azienda: dict
    data: str
    prestazione: dict
    differita: bool
    modulo: str
    associazione: str
    cittadino: dict
    prenotatoIl: str
    registratoIl: str
    modificatoIl: str
    annullatoIl: str
    noteAnnullamento: str
    stato: str
    tipo: str
    unitaErogante: dict
    unitaErogatrice: dict
    agenda: dict
    infoNote: dict
    infoNotePreparazione: dict
    infoLuogoPresentazione: dict
    infoMemorandum: dict
    infoNoteDisdettaPrenotazione: dict
    infoConsensoInformato: dict
    infoMezzi: dict
    cicli: list
    quesitoDiagnostico: dict
    regimeErogazione: str
    risorsa: str
    tariffaLp: str

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
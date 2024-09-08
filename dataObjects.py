from datetime import datetime

class Patient:
    def __init__(self, codice_fiscale: str, tessera_sanitaria: str):
        self.codice_fiscale = codice_fiscale
        self.tessera_sanitaria = tessera_sanitaria


class Prescription:
    def __init__(self, prescription_n: str, patient: Patient):
        # Initialize the prescription with the code
        self.prescription_n = prescription_n
        self.codice_fiscale = patient.codice_fiscale
        self.tessera_sanitaria = patient.tessera_sanitaria


class Appointment:
    def __init__(self, date: str, address: str, prescription: Prescription):
        # Initialize the appointment with date, address and prescription
        self.date = date
        self.address = address
        self.prescription = prescription
    
    def change_app(self, new_date: str, new_address: str):
        self.date = new_date
        self.address = new_address

    def get_datetime(self):
        return datetime.strptime(self.date, "%d/%m/%Y - %H:%M")


class SearchPreferences:
    def __init__(self, provincia, start_date, end_date, refresh_frequency):
        self.provincia = provincia
        self.start_date = start_date
        self.end_date = end_date
        self.refresh_frequency = refresh_frequency
    
    def get_start_date_input(self):
        return ''.join(filter(str.isdigit, self.start_date))

    def get_start_date_datetime(self):
        return datetime.strptime(self.start_date, "%d/%m/%Y")
    
    def get_end_date_datetime(self):
        return datetime.strptime(self.end_date, "%d/%m/%Y")
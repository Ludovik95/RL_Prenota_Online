class Patient:
    def __init__(self, codice_fiscale, tessera_sanitaria):
        self.codice_fiscale = codice_fiscale
        self.tessera_sanitaria = tessera_sanitaria


class Prescription:
    def __init__(self, prescription_n, patient):
        """ Initialize the prescription with the code """
        self.prescription_n = prescription_n
        self.codice_fiscale = patient.codice_fiscale
        self.tessera_sanitaria = patient.tessera_sanitaria


class Appointment:
    def __init__(self, date, address, prescription):
        """ Initialize the appointment with date, address and prescription """
        self.date = date
        self.address = address
        self.prescription = prescription
    
    def change_app(self, new_date, new_address):
        self.date = new_date
        self.address = new_address


class SearchPreferences:
    def __init__(self, provincia, start_date, refresh_frequency):
        self.provincia = provincia
        self.start_date = start_date
        self.refresh_frequency = refresh_frequency
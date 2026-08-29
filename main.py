from client import Client
import client
from objects import Patient, Prescription, Appointment
import argparse

def main(args):

    client = Client(debug=args.debug)

    codice_fiscale = input("Inserisci il codice fiscale: ").upper()
    codice_tessera = input("Inserisci le ultime 5 cifre della tessera sanitaria: ")
    id_ricetta = input("Inserisci il codice della ricetta: ").upper()
    provincia = input("Inserisci la provincia dove cercare l'appuntamento: ").upper()

    patient = client.login(codice_fiscale, codice_tessera)
    current_appointment = client.get_appointment(patient.codice_fiscale, id_ricetta)
    prescription = client.get_prescription(patient.codice_fiscale, id_ricetta)

    client.get_availability(patient, prescription, provincia)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    main(args)
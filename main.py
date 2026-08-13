from client import Client
from objects import Patient, Prescription, Appointment
import argparse

def main(args):

    client = Client(debug=args.debug)

    codice_fiscale = input("Inserisci il codice fiscale: ")
    codice_tessera = input("Inserisci le ultime 5 cifre della tessera sanitaria: ")
    prescription_n = input("Inserisci il codice della ricetta: ")

    patient = Patient(codice_fiscale,codice_tessera)

    client.login(patient.codice_fiscale, patient.codice_tessera)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    main(args)
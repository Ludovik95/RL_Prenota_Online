from client import Client
import client
from objects import Patient, Prescription, Appointment
import argparse

def main(args):

    client = Client(debug=args.debug)

    codiceFiscale = input("Inserisci il codice fiscale: ").upper()
    crs = input("Inserisci le ultime 5 cifre della tessera sanitaria: ")
    id_ricetta = input("Inserisci il codice della ricetta: ").upper()
    provincia = input("Inserisci la provincia dove cercare l'appuntamento: ").upper()

    patient = client.login(codiceFiscale, crs)
    if not patient:
        print("Errore durante il login")
        return

    current_appointment = client.get_appointment(patient.codiceFiscale, id_ricetta)
    prescription = client.get_prescription(patient.codiceFiscale, id_ricetta)

    appointment_list = client.get_availability(patient, prescription, provincia)
    appointment_list = sorted(appointment_list, key=lambda x: x["appuntamento"]["data"])
    new_appointment = Appointment.from_dict(appointment_list[0]["appuntamento"])
    if new_appointment.get_data() < current_appointment.get_data():
        print(f"Nuovo appuntamento disponibile: {new_appointment.get_data()}")
        print(f"Presso: {new_appointment.unitaErogante["presidio"]["descrizione"]}")
        print(f"Prenotazione attuale: {current_appointment.get_data()}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    main(args)
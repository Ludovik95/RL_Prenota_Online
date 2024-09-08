### ISTRUZIONI ###
# Per utilizzare questo file al posto dell'inserimento manuale tramite prompt dei comandi, 
# sostituisci i valori delle variabili sotto e rinomina il file in 'data_file.py'.
#
# Nel file main.py, metti in commento 'prescription, search_preferences = ask_data()'
# e togli dai commenti 'prescription, search_preferences = get_data()'.


codice_fiscale = "AAAAAA00A00A000A"     # codice fiscale associato alla ricetta
tessera_sanitaria = "00000"             # gli ultimi 5 numeri della tessera sanitaria, sul retro
prescription_n = "00000000000000"       # codice numerico della ricetta
provincia = "MILANO CITTA'"             # zona di ricerca (copia uno dei valori dalla lista sotto)
start_date = "00/00/0000"               # data di inizio ricerca in gg/mm/aaaa
end_date = "00/00/0000"                 # data di fine ricerca in gg/mm/aaaa
refresh_frequency = 60                  # secondi di pausa tra una ricerca e la successiva


### PROVINCE ###
"""
BERGAMO
BRESCIA
COMO
CREMONA
LECCO
LODI
MANTOVA
MILANO CITTA'
MILANO PROVINCIA
MONZA E DELLA BRIANZA
PAVIA
SONDRIO
VARESE
"""

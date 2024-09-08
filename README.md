# RL Prenota Online
## Che cos'è RL Prenota Online
La sanità in Lombardia sta diventando sempre più privata, e le disponibilità di visita nel SSN sempre più limitate. 
Molto spesso chi deve prenotare delle visite di controllo deve aspettare molti mesi, se non un anno e più, e per le urgenze si è obbligati a rivolgersi a cliniche private con ***costi allucinanti***. 
Quando si hanno molte patologie, queste pratiche diventano dispendiose in termini di tempo e soldi, e questo ***danneggia la parte più vulnerabile della popolazione***.

Alcune volte capita che delle visite tornino disponibili per modifiche di appuntamento di altri cittadini. Non sempre è semplice individuarli e prenotarli per tempo: la maggior parte delle disponibilità spariscono dopo poco perché qualcun altro è stato più veloce. 
L'unico modo per non avere la visita dopo un anno è entrare sul sito di prenotazione ogni giorno e continuare ad aggiornare la pagina, nella speranza che si liberi un posto. Oppure chiamando il numero regionale del CUP continuamente. Insomma, un secondo lavoro che ***in pochissimi possono permettersi***.

RL Prenota Online permette di automatizzare la ricerca di nuovi appuntamenti nel sistema di prenotazione online delle visite mediche in Regione Lombardia. 
I dati rimangono nel proprio device e non vengono trasmessi a terzi se non durante l'immissione nel sito di prenotazione (quello che accadrebbe facendo i passaggi manualmente).


## Installazione dei prerequisiti
Per utilizzare RL Prenota Online bisogna installare sul proprio computer Python e Selenium.
Una volta installato Python e pip, basterà aprire il prompt dei comandi e digitare `pip install -U selenium`.


## Come usarlo
Apri un prompt dei comandi nella cartella principale e avvia il codice digitando `py main.py`. 
Ti verranno chiesti il codice fiscale, gli ultimi 5 numeri della tessera sanitaria e il codice della ricetta (solo numeri, senza inserire lettere). 
A quel punto verranno cercate nuove disponibilità per la visita nella provincia e dalla data inserita. In caso positivo, sempre sul terminale verrà chiesta la conferma di modifica dell'appuntamento.

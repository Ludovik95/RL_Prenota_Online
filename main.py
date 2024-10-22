from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime
import time
import sys
from dataObjects import Patient, Prescription, Appointment, SearchPreferences
import data_file
from os import path

def ask_data():
    codice_fiscale = input("Inserisci il codice fiscale: ")

    tessera_sanitaria = input("Inserisci le ultime 5 cifre della tessera sanitaria: ")
    prescription_n = input("Inserisci il codice della ricetta: ")
    
    print ("Inserisci la provincia in cui vuoi la visita tra le seguenti: BERGAMO, BRESCIA, COMO, CREMONA, LECCO, LODI, MANTOVA, MILANO CITTA', MILANO PROVINCIA, MONZA E DELLA BRIANZA, PAVIA, SONDRIO, VARESE")
    provincia = input("").upper()
    start_date = input("Inserisci la prima data da cui vuoi la visita (gg/mm/aaaa): ")
    end_date = input("Inserisci la data entro cui vuoi la visita (gg/mm/aaaa): ")
    REFRESH_FREQUENCY = int(input("Inserisci ogni quanti secondi riavviare la ricerca se non è stata trovata una data: "))

    print("\n")

    patient = Patient(codice_fiscale, tessera_sanitaria)
    prescription = Prescription(prescription_n, patient)
    search_preferences = SearchPreferences(provincia, start_date, end_date, REFRESH_FREQUENCY)

    return prescription, search_preferences


def get_data_from_file():
    patient = Patient(data_file.codice_fiscale, data_file.tessera_sanitaria)
    prescription = Prescription(data_file.prescription_n, patient)
    search_preferences = SearchPreferences(data_file.provincia, data_file.start_date, data_file.end_date,data_file.refresh_frequency)

    return prescription, search_preferences


def use_chrome():
    # initialize Chrome webdriver
    options = Options()
    options.add_argument("--log-level=1")
    # keep the browser open after the process has ended, so long as the quit command is not sent to the driver.
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    return driver


def use_firefox():
    # initialize Firefox webdriver
    driver = webdriver.Firefox()
    return driver


def get_current_appointment(driver, ignored_exceptions, prescription):
    # Get the element with all info
    appointment_data = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dati-appuntamento-summary")))
    
    # Get appointment date and address
    app_date_string = appointment_data.find_element(By.XPATH, "div[6]/div[2]/span").text
    address = appointment_data.find_element(By.XPATH, "div[4]/div[2]/span").text
    
    return Appointment(app_date_string, address, prescription)


def wait_loading(driver):
    # Wait for spinner to appear and disappear
    try:
        # wait for loading element to appear
        WebDriverWait(driver, 10
            ).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".spinner-container")))

        # then wait for the element to disappear
        WebDriverWait(driver, 120
            ).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".spinner-container")))

    except TimeoutException:
        # if timeout exception was raised
        pass 


def get_first_availability(driver, ignored_exceptions):

    # Get appointment list
    app_list = WebDriverWait(driver, 60, ignored_exceptions=ignored_exceptions)\
        .until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".lista-appuntamenti")))

    # Get first availability date
    first_availability_string = driver.find_element(By.XPATH, "//ul/li/div/div/div[1]/div[2]/span").text
    first_availability = datetime.strptime(first_availability_string, "%d/%m/%Y - %H:%M")
    return first_availability


def get_new_appointment_info(driver, ignored_exceptions):
    appointment_data = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dati-appuntamento-summary")))
    new_address = appointment_data.find_element(By.XPATH, "div[3]/div[2]/span").text
    new_date = appointment_data.find_element(By.XPATH, "div[1]/div[2]/span").text
    alert = driver.find_elements(By.CSS_SELECTOR, ".note-prepazione-descrizione > p")
    return new_address, new_date, alert


def main():
    print("ciao :) \n")

    # Ask user information that will be used during search
    if path.isfile("data_file.py"):
        if input("Scrivi 1 per inserire i dati a mano oppure 2 per utilizzare quelli nel file 'data_file.py': ") == "2":
            prescription, search_preferences = get_data_from_file()
        else:
            prescription, search_preferences = ask_data()  
    else:
        prescription, search_preferences = ask_data()
    

    # Ask which browser to use
    driver = use_chrome() if input("Scrivi 1 per usare Chrome oppure 2 per Firefox: ") == "1" else use_firefox()
    driver.set_window_size(1400,1000)

    # Open link Prenota Online
    driver.get("https://prenotasalute.regione.lombardia.it/prenotaonline/")
         

    try:
        # Go to Gestione prenotazioni
        ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
        element = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[ui-sref='prenota-ricetta']")))
        actions = ActionChains(driver)
        actions.double_click(element).perform()

        # Enter patient and prescription data
        driver.find_element(By.ID, "cf").send_keys(prescription.codice_fiscale)
        driver.find_element(By.ID, "crs").send_keys(prescription.tessera_sanitaria)
        driver.find_element(By.ID, "codice").send_keys(prescription.prescription_n)

        # Confirm data
        element = driver.find_element(By.XPATH, "//button[@type='submit']")
        actions = ActionChains(driver)
        actions.double_click(element).perform()



        # Get current appointment date
        current_appointment = get_current_appointment(driver, ignored_exceptions, prescription)
        print("L'appuntamento attuale è fissato per il giorno", current_appointment.date)
        print("presso", current_appointment.address)
        print("\n")


        # Click on edit appointment 
        element = driver.find_element(By.CSS_SELECTOR, "button[btn-riprenota='']")
        actions = ActionChains(driver)
        actions.double_click(element).perform()

        # Confirm modal 
        WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-footer > .btn-primary[ng-click^='riprenotaRicettaCtrl.conferma']"))).click()



        # Select search area
        element = Select(WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[id='provincia']"))))
        element.select_by_visible_text(search_preferences.provincia)

        # Select start data
        start_date_str = search_preferences.get_start_date_input()
        driver.find_element(By.ID, "quando").send_keys(start_date_str)

        # Confirm filters
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = driver.find_element(By.CSS_SELECTOR, ".submit")
        actions = ActionChains(driver)
        actions.double_click(element).perform()

        ### Check if any alert popup appear ###


        stop_searching = False

        while stop_searching == False:
            # Get first availability date
            first_availability = get_first_availability(driver, ignored_exceptions)
           
            # Check if first date is before current appointment date
            if first_availability < current_appointment.get_datetime() or current_appointment.get_datetime() < search_preferences.get_start_date_datetime():
                driver.find_element(By.CSS_SELECTOR, ".ui-disponibilita-action-buttons > button[id='verifica_conferma_appuntamenti']").click()

                # Get appointment info
                new_address, new_date, alert = get_new_appointment_info(driver, ignored_exceptions)
                
                print("È disponibile un appuntamento per il giorno", new_date)
                print("presso", new_address)
                if alert:
                    print("Sono presenti le seguenti note: \n")
                    for a in alert:
                        print(a.text, "\n")


                risposta = input("Vuoi confermare il nuovo appuntamento? Y/N ")

                if risposta == "Y":
                    driver.find_element(By.CSS_SELECTOR, ".checkmark").click()
                    # Confirm modal 
                    WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
                        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-footer > .btn-primary[ng-click^='verificaPrenotazioneCtrl.conferma']"))).click()
                    
                    ###
                    ### To do: Check if new appointment is confirmed or not ###
                    ###

                    # Update current appointment
                    current_appointment.change_app(first_availability, new_address)
                    
                risposta = input("Vuoi continuare la ricerca? Y/N ")

                if risposta == "N":
                    stop_searching = True
                    break
                else:
                    # Close modal 
                    driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-default[ng-click^='verificaPrenotazioneCtrl.annulla']").click()
            
            # Wait timeout
            print("Fra {} secondi partirà la nuova ricerca".format(search_preferences.refresh_frequency))
            time.sleep(search_preferences.refresh_frequency)

            # Click on edit search button
            element = driver.find_element(By.CSS_SELECTOR, "button[id='modifica-ricerca-info-testata']")
            actions = ActionChains(driver)
            actions.move_to_element(element).click(element).perform()

            # Confirm modal and search again
            element = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-footer > .btn-primary[ng-click^='doveQuandoModalCtrl.aggiorna']")))
            actions = ActionChains(driver)
            actions.move_to_element(element).click(element).perform()

            wait_loading(driver)

        
        # Close the browser and end script
        print("Grazie per aver combattuto insieme contro la sanità privata <3")
        driver.quit()
        sys.exit()

    except Exception as e:
        print(e)

#    # select strutture
#    driver.find_element(By.CSS_SELECTOR, ".filter-fieldset:nth-child(2) .glyphicon").click()
#    driver.find_element(By.CSS_SELECTOR, "#strutture .ui-select-search").click()
#    driver.find_element(By.CSS_SELECTOR, "#ui-select-choices-row-0-0 .ng-binding").click()
#    # select sedi
#    driver.find_element(By.CSS_SELECTOR, "a > .glyphicon-chevron-right").click()
#    driver.find_element(By.CSS_SELECTOR, "#sedi .ui-select-search").click()
#    driver.find_element(By.CSS_SELECTOR, "#ui-select-choices-row-1-0 .ng-binding").click()
#


if __name__ == "__main__":
    main()
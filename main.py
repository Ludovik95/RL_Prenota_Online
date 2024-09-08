from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime
import time
import sys
from dataObjects import Patient, Prescription, Appointment, SearchPreferences
import data_file

def main():
    print("ciao :) \n")

    # Ask user information that will be used during search
    prescription, search_preferences = ask_data()
    # prescription, search_preferences = get_data()


    # Ask which browser to use
    driver = use_chrome() if input("Scrivi 1 per usare Chrome oppure 2 per Firefox: ") == 1 else use_firefox()
    driver.set_window_size(1400,800)

    # Open link Prenota Online
    driver.get("https://prenotasalute.regione.lombardia.it/prenotaonline/")
         
    try:
        # Go to Gestione prenotazioni
        ignored_exceptions = (NoSuchElementException,StaleElementReferenceException,)
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


        is_new_appointment = False

        while is_new_appointment == False:
            # Get first availability date
            first_availability = get_first_availability(driver, ignored_exceptions)
           
            # Check if first date is before current appointment date
            if first_availability < current_appointment.get_datetime() or current_appointment.get_datetime() < search_preferences.get_start_date_datetime():
                driver.find_element(By.CSS_SELECTOR, ".ui-disponibilita-action-buttons > button[id='verifica_conferma_appuntamenti']").click()

                # Get appointment info
                new_address, new_date = get_new_appointment_info(driver, ignored_exceptions)
                
                print("È disponibile il seguente appuntamento:")
                print(new_date)
                print(new_address)

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
                    is_new_appointment = True
                else:
                    # Close modal 
                    driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-default[ng-click^='verificaPrenotazioneCtrl.annulla']").click()
            
            # Wait timeout
            print("Fra {} secondi partirà la nuova ricerca".format(search_preferences.refresh_frequency))
            time.sleep(search_preferences.refresh_frequency)

            # Click on edit search button
            driver.find_element(By.CSS_SELECTOR, "button[id='modifica-ricerca-info-testata']").click()

            # Confirm modal and search again
            WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-footer > .btn-primary[ng-click^='doveQuandoModalCtrl.aggiorna']"))).click()

        
        # Close the browser and end script
        print("Grazie per aver combattuto insieme la sanità privata <3")
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


def ask_data():
    codice_fiscale = input("Inserisci il codice fiscale: ")

    tessera_sanitaria = input("Inserisci le ultime 5 cifre della tessera sanitaria: ")
    prescription_n = input("Inserisci il codice NUMERICO della ricetta: ")
    
    provincia = input("Inserisci la provincia in cui vuoi la visita: ")
    start_date = input("Inserisci la prima data da cui vuoi la visita (gg/mm/aaaa): ")
    end_date = input("Inserisci la data entro cui vuoi la visita (gg/mm/aaaa): ")
    refresh_frequency = int(input("Inserisci ogni quanti secondi riavviare la ricerca se non è stata trovata una data: "))

    patient = Patient(codice_fiscale, tessera_sanitaria)
    prescription = Prescription(prescription_n, patient)
    search_preferences = SearchPreferences(provincia, start_date, end_date, refresh_frequency)

    return prescription, search_preferences


def get_data():
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


def get_first_availability(driver, ignored_exceptions):
    # Get appointment list
    ### Non deve leggere il contenuto della pagina se c'è ancora lo spinner/loader ###
    # WebDriverWait(driver, 60, ignored_exceptions=ignored_exceptions)\
    #     .until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".spinner-container")))
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
    return new_address, new_date


if __name__ == "__main__":
    main()
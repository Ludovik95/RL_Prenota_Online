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
import data_file

def main():
    print("ciao")

    codice_fiscale = input("Inserisci il codice fiscale:")
    tessera_sanitaria = input("Inserisci le ultime 5 cifre della tessera sanitaria:")
    prescription_n = input("Inserisci il codice NUMERICO della ricetta:")
    provincia = input("Inserisci la provincia in cui vuoi la visita:")
    data_iniziale = input("Inserisci la prima data da cui vuoi la visita:")
    refresh_frequency = input("Inserisci ogni quanti secondi riavviare la ricerca se non è stata trovata una data:")

    # codice_fiscale = data_file.codice_fiscale
    # tessera_sanitaria = data_file.tessera_sanitaria
    # prescription_n = data_file.prescription_n
    # provincia = data_file.provincia
    # data_iniziale = data_file.data_iniziale
    # refresh_frequency = data_file.refresh_frequency

    # start webdriver (opens a new window)
    driver = webdriver.Firefox()
    driver.set_window_size(1400,800)

    # open link Prenota Online
    driver.get("https://prenotasalute.regione.lombardia.it/prenotaonline/")
         
    try:
        # Go to Gestione prenotazioni
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        element = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[ui-sref='prenota-ricetta']")))
        actions = ActionChains(driver)
        actions.double_click(element).perform()

        # Enter data
        driver.find_element(By.ID, "cf").send_keys(codice_fiscale)
        driver.find_element(By.ID, "crs").send_keys(tessera_sanitaria)
        driver.find_element(By.ID, "codice").send_keys(prescription_n)

        # Confirm data
        element = driver.find_element(By.XPATH, "//button[@type='submit']")
        actions = ActionChains(driver)
        actions.double_click(element).perform()



        # Get current appointment date
        app_date_string = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[ng-if^='appuntamentoCtrl.appunificato.appuntamenti[0].data'] > .appuntamento-field-value > .ng-binding"))).text
        print(app_date_string)
        app_date = datetime.strptime(app_date_string, "%d/%m/%Y - %H:%M")
        print(app_date)

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
        element.select_by_visible_text(provincia)

        # Select start data
        driver.find_element(By.ID, "quando").send_keys(data_iniziale)

        # Confirm filters
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = driver.find_element(By.CSS_SELECTOR, ".submit")
        actions = ActionChains(driver)
        actions.double_click(element).perform()

        # Get appointment list
        app_list = WebDriverWait(driver, 60, ignored_exceptions=ignored_exceptions)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lista-appuntamenti")))
        print("done")

        # Get first availability date
        first_availability_string = driver.find_element(By.XPATH, "//ul/li/div/div/div[1]/div[2]/span").text
        first_availability = datetime.strptime(first_availability_string, "%d/%m/%Y - %H:%M")
        
        # Check if first date is before current appointment date
        if first_availability < app_date:
            driver.find_element(By.CSS_SELECTOR, ".ui-disponibilita-action-buttons > button[id='verifica_conferma_appuntamenti']").click()
            print("È disponibile il seguente appuntamento:")
            print(first_availability)
            print(driver.find_element(By.XPATH, "//ul/li/div/div/div[2]/div[2]/span").text)
            print(driver.find_element(By.XPATH, "//ul/li/div/div/div[3]/div[2]/span").text)
            print(driver.find_element(By.XPATH, "//ul/li/div/div/div[4]/div[2]/span").text)
            risposta = input("Vuoi confermare il nuovo appuntamento? Y/N")

            if risposta == "Y":
                driver.find_element(By.CSS_SELECTOR, ".checkmark").click()
                ### Click on button ###
                ### Check if new appointment is confirmed or not ###
            else:
                time.sleep(refresh_frequency)
                driver.refresh()
                ### Check again first availability ###
        else:
            time.sleep(refresh_frequency)
            driver.refresh()
            ### Check again first availability ###




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
    ### check first date if before appointment date ###
    ### if yes, try to book ###
        ### ask the user if it is ok ###
            ### js = 'alert("Hello World")'
            ### driver.execute_script(js)
        ### if booked, send notification to user ###
    ### if not, wait 120 seconds and refresh page ###

    # Refresh page to check new dates
    ### driver.refresh()

    # End script closing the browser
#    driver.quit()

if __name__ == "__main__":
    main()
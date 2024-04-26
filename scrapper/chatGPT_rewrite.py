import json
import time
import undetected_chromedriver as uc
import configparser

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

CONFIG_FILE_NAME = "../../scrapper.ini"

DOCUMENTS_PATH = "../documents/"
SPANISH_ABSTRACTS_FILENAME = "spanish_abstracts.txt"
REWRITTEN_SPANISH_ABSTRACTS_FILENAME = "rewritten_spanish_abstracts.txt"

CHAT_ROLE_PROMPT = "Voy a pasarte varios textos. Tu tarea consiste en comprender y reescribir esos textos con tus palabras."
MAX_SIZE = 3000

config = None

chrome = None
input_area = None
prompt_area = None

spanish_abstracts_file = open(
    DOCUMENTS_PATH + SPANISH_ABSTRACTS_FILENAME,
    "r",
    encoding='utf-8'
)
rewritten_spanish_abstracts_file = open(
    DOCUMENTS_PATH + REWRITTEN_SPANISH_ABSTRACTS_FILENAME,
    "a",
    encoding='utf-8'
)

def initiate_chat(account_option: int):
    chrome = login(account_option)

    prompt_area = chrome.find_element(By.TAG_NAME, "textarea")
    input_area = prompt_area.find_element(By.XPATH, "..")
    
    send_message(CHAT_ROLE_PROMPT, prompt_area, input_area)
    
    return prompt_area, input_area

def login(account_option: int):
    chrome.get("https://chat.openai.com/chat")
    
    login_button = chrome.find_elements(By.TAG_NAME, "button")[0]
    login_button.click()
    
    time.sleep(2)

    google_button = chrome.find_elements(By.CLASS_NAME, "social-btn")[0]
    google_button.click()
    
    time.sleep(2)
    
    email_input = chrome.find_element(By.NAME, "identifier")
    if account_option == 0:
        email_input.send_keys(config["USERS"]["USER1"])
    else:
        email_input.send_keys(config["USERS"]["USER2"])
    
    for button in chrome.find_elements(By.TAG_NAME, "button"):
        try:
            button_span = button.find_element(By.TAG_NAME, "span")
            if button_span.text == "Siguiente":
                button.click()
                break
        except:
            pass

    time.sleep(5)
    
    passwd_input = chrome.find_element(By.NAME, "Passwd")
    if account_option == 0:
        passwd_input.send_keys(config["USERS"]["PASSWD1"])
    else:
        passwd_input.send_keys(config["USERS"]["PASSWD2"])
    
    
    for button in chrome.find_elements(By.TAG_NAME, "button"):
        try:
            button_span = button.find_element(By.TAG_NAME, "span")
            if button_span.text == "Siguiente":
                button.click()
                break
        except:
            pass

    time.sleep(15)
    
    return chrome

def send_message(
    text: str,
    prompt_area: WebElement,
    input_area: WebElement
):  
    time_to_wait = len(text) / MAX_SIZE * 15
    if time_to_wait < 5:    
        time_to_wait = 5
    
    print("Escribiendo texto...")
    prompt_area.clear()
    prompt_area.send_keys(text)
    
    print("Enviando....")
    send_prompt_button = input_area.find_element(By.TAG_NAME, "button")
    send_prompt_button.click()
    time.sleep(time_to_wait + 5)
    
    print("Leyendo respuesta...")
    response_div = chrome.find_elements(By.CLASS_NAME, "markdown")[-1]
    
    return response_div.text
        
if __name__ == '__main__':    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)
    
    try:    
        num_abstracts = 0
        last_abstract = 0
        max_abstracts = 0
        num_session_abstracts = 0
        
        account_option = 0
        chrome = uc.Chrome()
        prompt_area, input_area = initiate_chat(account_option)

        for abstract_data_row in spanish_abstracts_file.readlines()[::-1]:
            
            if len(abstract_data_row) > MAX_SIZE:
                    continue
            
            num_abstracts += 1
            if num_abstracts <= last_abstract:
                continue
            
            num_session_abstracts += 1
            if num_session_abstracts > 40:
                chrome.close()
                chrome.quit()
                num_session_abstracts = 0
                
                account_option = (account_option + 1) % 2
                chrome = uc.Chrome()
                prompt_area, input_area = initiate_chat(account_option)
            
            try:       
                perc = round(num_abstracts / max_abstracts * 100, 2)  
                print(f"\n{num_abstracts} - ({perc}%)")
                
                abstract_data = json.loads(abstract_data_row[:-2])
                
                current_time = time.strftime("%H:%M:%S", time.gmtime())
                print(f"{current_time}")
                
                abstract_data["Resumen_ChatGPT"] = send_message(
                    abstract_data["Resumen"],
                    prompt_area,
                    input_area)
                
                rewritten_spanish_abstracts_file.write(
                    f"{str(abstract_data)},\n"
                )
                
                if num_abstracts == max_abstracts:
                    break
                
            except:
                break
            
    finally:
        rewritten_spanish_abstracts_file.close()
        spanish_abstracts_file.close()
        chrome.close()
        chrome.quit()
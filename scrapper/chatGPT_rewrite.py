import json
import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By

chrome = uc.Chrome()
prompt_area = None
send_prompt_button = None

spanish_abstracts_file = \
    open("spanish_abstracts.txt", "r", encoding='utf-8')
rewritten_spanish_abstracts_file = \
    open("rewritten_spanish_abstracts.txt", "a", encoding='utf-8')

MESSAGE_END = "Se acabó el juego"

CHAT_ROLE_PROMPT = f"Voy a pasarte varios textos. Tu tarea consiste en comprender y reescribir esos textos con tus palabras. Cuando te escriba el mensaje '{MESSAGE_END}', tu tarea habrá terminado. Si lo has comprendido, escribe el mensaje de finalización"

def login():
    login_button = chrome.find_elements(By.TAG_NAME, "button")[0]
    login_button.click()
    
    time.sleep(2)

    google_button = chrome.find_elements(By.CLASS_NAME, "social-btn")[0]
    google_button.click()
    
    time.sleep(2)
    
    email_input = chrome.find_element(By.NAME, "identifier")
    email_input.send_keys("danicerrato2000")
    
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
    passwd_input.send_keys("Acertaste2?")
    
    for button in chrome.find_elements(By.TAG_NAME, "button"):
        try:
            button_span = button.find_element(By.TAG_NAME, "span")
            if button_span.text == "Siguiente":
                button.click()
                break
        except:
            pass

    time.sleep(15)

def send_message(text: str) -> str:
    prompt_area.clear()
    prompt_area.send_keys(text)
    send_prompt_button.click()
    
    time.sleep(20)
    
    response_div = chrome.find_elements(By.CLASS_NAME, "agent-turn")[-1]
    response = response_div.find_element(By.TAG_NAME, "p")
    
    return response.text

if __name__ == '__main__':
    chrome.get("https://chat.openai.com/chat")
    
    try:
        login()

        prompt_area = chrome.find_element(By.TAG_NAME, "textarea")
        input_area = prompt_area.find_element(By.XPATH, "..")
        send_prompt_button = \
            input_area.find_element(By.TAG_NAME, "button")
            
        response = send_message(CHAT_ROLE_PROMPT)
        if not response.__contains__(MESSAGE_END):
            print("No continuar")
            exit()
        
        for abstract_data_row in spanish_abstracts_file.readlines():
            try:
                abstract_data = json.loads(abstract_data_row[:-2])
                
                abstract_data["Resumen_ChatGPT"] = \
                    send_message(abstract_data["Resumen"])
                
                rewritten_spanish_abstracts_file.write(
                    f"{str(abstract_data)},\n"
                )
            except:
                pass
        
    finally:
        spanish_abstracts_file.close()
        chrome.close()
        chrome.quit()
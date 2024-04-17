from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import undetected_chromedriver as uc

chrome = uc.Chrome()

def login():
    login_button = chrome.find_elements(By.Tag_name)

if __name__ == '__main__':
    chrome.get("https://chat.openai.com/chat")
    
    try:
        login()
    
    finally:
        chrome.quit()
        chrome.exit()
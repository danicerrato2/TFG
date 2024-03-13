import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

def save_document_url(chrome, preview_url, urls_file):
    chrome.get(preview_url)
    
    # Recoger el enlace al documento
    columns = chrome.find_elements(
        by=By.CLASS_NAME,
        value="text-nowrap")
    for column in columns:
        try:
            pdf_link = column.find_element(
                by=By.TAG_NAME,
                value="a")
            
            pdf_url = pdf_link.get_attribute("href")
            urls_file.write(pdf_url + "\n")

        except: 
            pass


if __name__ == '__main__':
    chrome_service = webdriver.ChromeService(
        executable_path='.\\chromedriver.exe')
    webdriver.ChromeOptions().binary_location = \
    	'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    chrome = webdriver.Chrome(service=chrome_service)

    # Entrar a la página
    chrome.get('https://idus.us.es/handle/11441/11441/browse?type=dateissued')

    try:
        # Seleccionar el año
        year_browser = chrome.find_element(by=By.NAME, value="year")
        selector = Select(year_browser)
        selector.select_by_visible_text('2016')
        
        num_documents = 0
        document_preview_urls = []
        while num_documents < 1000:
            # Conseguir los enlaces a las vistas previas de cada documento
            artifacts = chrome.find_elements(
                by=By.CLASS_NAME,
                value='artifact-title')
            
            for artifact in artifacts:
                link = artifact.find_element(by=By.TAG_NAME, value='a')
                document_preview_urls.append(link.get_attribute("href"))
                
                num_documents += 1
            
            # Al conseguir los 20 enlaces, pasamos a la siguiente pagina
            previous_page = chrome.find_element(
                by=By.CLASS_NAME,
                value="previous-page-link")
            chrome.get(previous_page.get_attribute('href'))
        
        with open("document_urls.txt", 'w') as f:
            for document_preview in document_preview_urls:
                save_document_url(chrome, document_preview, f)
        
    except:
        pass

    finally:
        chrome.close()
        chrome.quit()

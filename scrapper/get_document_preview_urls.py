from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


if __name__ == '__main__':
    chrome_service = webdriver.ChromeService(
        executable_path='.\\chromedriver_123-0-6309-0.exe')
    chrome = webdriver.Chrome(service=chrome_service)

    # Entrar a la página
    chrome.get('https://idus.us.es/handle/11441/11441/browse?type=dateissued')

    document_preview_urls = []
    preview_urls_file = open("document_preview_urls.txt", "w")
    try:
        # Seleccionar el año
        year_browser = chrome.find_element(by=By.NAME, value="year")
        selector = Select(year_browser)
        selector.select_by_visible_text('2024')
        
        finished = False
        while finished == False:
            # Conseguir los enlaces a las vistas previas de cada documento
            artifacts = chrome.find_elements(
                by=By.CLASS_NAME,
                value='artifact-title')
            
            for artifact in artifacts:
                link = artifact.find_element(by=By.TAG_NAME, value='a')
                preview_url = link.get_attribute("href")
                preview_urls_file.write(f"{preview_url}\n")
                document_preview_urls.append(preview_url)
            
            # Al conseguir los 20 enlaces, pasamos a la siguiente pagina
            previous_page = chrome.find_element(
                by=By.CLASS_NAME,
                value="previous-page-link")
            chrome.get(previous_page.get_attribute('href'))
    except:
        finished = True
        preview_urls_file.close()

    finally:
        chrome.close()
        chrome.quit()

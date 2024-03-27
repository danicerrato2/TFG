from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

def save_document_data(chrome: webdriver.Chrome, preview_url, data_file):
    chrome.get(preview_url)
    
    document_data = {
        "Idus_URL": preview_url,
        "Type": "",
        "Title": "",
        "Autor/es": "",
        "Director/es": "",
        "Publicacion": "",
        "Resumenes": {},
        "PDF_URL": ""
    }
    
    error_file = open("error_logs.txt", "w")
    
    # Recoger Tipo de documento
    try:
        document_type = chrome.find_element(by=By.TAG_NAME, value='h3')
        document_data["Type"] = document_type.text    
    except:
        error_file.write(f"{preview_url}: Type\n")
    
    # Recoger Nombre del documento
    try:
        document_title = chrome.find_element(by=By.TAG_NAME, value="h2")
        document_data["Title"] = \
            document_title.find_element(by=By.TAG_NAME, value="div").text
    except:
        error_file.write(f"{preview_url}: Title\n")
        
    # Miramos la tabla de datos del documento
    try:
        info_rows = chrome.find_elements(
            by=By.CLASS_NAME,
            value="ds-table-row")
        
        for row in info_rows:
            section = None
            
            # Miramos las dos columnas de cada fila (a.k.a: <clave, valor>)
            for column in row.find_elements(by=By.TAG_NAME, value="td"):
                # La primera columna es la clave
                if section is None:
                    section = column.find_element(
                            by=By.CLASS_NAME,
                            value="bold"
                        ).text
                    continue
                
                # La segunda es el valor
                
                # Recoger Autor/es
                if section == "Autor/es":
                    try:
                        authors = column.find_elements(
                                by=By.TAG_NAME,
                                value="span")
                        
                        authors_list = []
                        for author in authors:
                            author_name = author.find_elements(
                                    by=By.TAG_NAME,
                                    value="a"
                                )[0]
                            authors_list.append(author_name.text)
                        
                        document_data["Autor/es"] = str.join('|', authors_list)
                    except:
                        error_file.write(f"{preview_url}: Autor/es\n")
                    
                # Recoger Directo/es
                elif section == "Director":
                    try:
                        directors = column.find_elements(
                                by=By.TAG_NAME,
                                value="span")
                        
                        directors_list = []
                        for director in directors:
                            director_name = director.find_elements(
                                    by=By.TAG_NAME,
                                    value="a"
                                )[0]
                            directors_list.append(director_name.text)
                        
                        document_data["Director/es"] = str.join('|', directors_list)
                    except:
                        error_file.write(f"{preview_url}: Director/es\n")
                
                # Recoger Fecha de publicacion
                elif section == "Fecha de publicación":
                    try:
                        document_data["Publicacion"] = column.text
                    except:
                        error_file.write(f"{preview_url}: Publicacion\n")
                
                # Recoger Resumen
                elif section == "Resumen":
                    try:
                        abstracts = column.find_elements(
                            by=By.TAG_NAME,
                            value="span")
                        
                        # Dividimos los resumenes cortos y largos
                        short_abstracts = []
                        long_abstracts = []
                        for abstract in abstracts:
                            display = abstract.value_of_css_property('display')
                            if display == 'inline':
                                short_abstracts.append(abstract)
                            elif display == 'none':
                                long_abstracts.append(abstract)
                        
                        # Hacemos que aparezcan en pantalla los resumenes largos
                        for abstract in short_abstracts:
                            link = abstract.find_element(
                                by=By.TAG_NAME,
                                value='a')
                            chrome.execute_script(link.get_attribute('href'))
                        
                        # Recogemos los resumenes largos
                        document_data["Resumenes"] = {}
                        i = 0
                        for abstract in long_abstracts:
                            try:
                                document_data["Resumenes"][f"Resumen_{i}"] = abstract.text
                            except:
                                error_file.write(
                                    f"{preview_url}: Resumen_{i}\n")
                            i += 1
                    except:
                        error_file.write(f"{preview_url}: Resumenes\n")
            
                section = None
    except:
        error_file.write(f"{preview_url}: Info table\n")
    
    # Recoger el enlace al documento
    try:
        tabla_pdf = chrome.find_element(
            by=By.CLASS_NAME,
            value="ds-table")
        pdf_link = tabla_pdf.find_elements(
            by=By.TAG_NAME,
            value="a")[0]
        document_data["PDF_URL"] = pdf_link.get_attribute("href")
    except: 
        error_file.write(f"{preview_url}: PDF_URL\n")
        
    data_file.write(f"{str(document_data)},\n")
    error_file.close()

if __name__ == '__main__':
    chrome_service = webdriver.ChromeService(
        executable_path='.\\chromedriver_123-0-6309-0.exe')
    chrome = webdriver.Chrome(service=chrome_service)
    
    with open("document_preview_urls.txt", 'r') as f:
        data_file = open("documents_data.txt", 'a', encoding='utf-8')
        
        total_files = 26300
        last_file = 16693
        
        try:
            for index, url in enumerate(f.readlines()[last_file:]):
                print(
                    f"{index + last_file} ({round((index + last_file) / total_files * 100, 2)}%)")
                save_document_data(chrome, url[:-1], data_file)
        except:
            pass
        finally:
            data_file.close()

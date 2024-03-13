import requests

downloads_path = 'D:\\DocumentosAcademicos\\'

with open("document_urls.txt", 'r') as f:
    for index, url in enumerate(f.readlines()):
        response = requests.get(url)
        
        with open(
            downloads_path + "document" + str(index) + '.pdf',
            'wb'
        ) as downloaded_file:
            downloaded_file.write(response.content)
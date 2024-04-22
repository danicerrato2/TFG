import langid
import json

documents_path = "../documents/"
documents_data_filename = "../documents_data.txt"
spanish_abstracts_filename = "spanish_abstracts.txt"
other_language_abstracts_filename = "other_language_abstracts.txt"

documents_data_file = open(
    documents_path + documents_data_filename,
    "r",
    encoding="utf-8"
)
spanish_abstracts_file = open(
    documents_path + spanish_abstracts_filename,
    "a",
    encoding='utf-8'
)
other_language_abstracts_file = open(
    documents_path + other_language_abstracts_filename,
    "a",
    encoding='utf-8'
)

if __name__ == '__main__':
    for document_data_row in documents_data_file.readlines():
        try:
            document_data = json.loads(document_data_row[:-2])
            
            if len(document_data["Resumenes"]) == 0:
                continue
            else:
                for abstract_id in document_data["Resumenes"].keys():
                    abstract_data = {}
                    abstract_data["Idus_URL"] = document_data["Idus_URL"]
                    abstract_data["id"] = abstract_id
                    
                    language, _ = langid.classify(
                        document_data["Resumenes"][abstract_id])
                    if language == 'es':
                        abstract_data["Resumen"] = \
                            document_data["Resumenes"][abstract_id]
                        spanish_abstracts_file.write(
                            f"{str(abstract_data)},\n"
                        )
                    else:
                        abstract_data["Idioma"] = language
                        other_language_abstracts_file.write(
                            f"{str(abstract_data)},\n"
                        )            
        except:
            pass
        
    documents_data_file.close()
    spanish_abstracts_file.close()
    other_language_abstracts_file.close()
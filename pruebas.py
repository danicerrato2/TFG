import json
import language_tool_python
import nltk

# from spellchecker import SpellChecker

DOCUMENTS_PATH = "documents/"
REWRITTEN_SPANISH_ABSTRACTS_FILENAME = "rewritten_spanish_abstracts.txt"
REWRITTEN_SPANISH_ABSTRACTS_STATS_FILENAME = "rewritten_spanish_abstracts_stats.txt"

PUNCTUATION_MARKS = [',', '.', ';', ':', '-']

rewritten_spanish_abstracts_file = open(
    DOCUMENTS_PATH + REWRITTEN_SPANISH_ABSTRACTS_FILENAME,
    "r",
    encoding='utf-8'
)

rewritten_spanish_abstracts_stats_file = open(
    DOCUMENTS_PATH + REWRITTEN_SPANISH_ABSTRACTS_STATS_FILENAME,
    "a",
    encoding='utf-8'
)

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

if __name__ == '__main__':
    # print(nltk.help.upenn_tagset())
    
    for abstract_data_row in rewritten_spanish_abstracts_file.readlines():
        abstract_data = json.loads(abstract_data_row[:-2])
        abstracts_stats = {
			"Idus_URL": abstract_data["Idus_URL"],
			"id": abstract_data["id"],
			"Resumen": {},
			"Resumen_ChatGPT": {}
		}
        
        original_abstract = abstract_data["Resumen"]
        
        tokens = word_tokenize(original_abstract)
        etiquetas_gramaticales = pos_tag(tokens)
        
        print(etiquetas_gramaticales)
            
        break
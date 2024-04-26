import json
import language_tool_python

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

if __name__ == '__main__':
    # checker = SpellChecker(language='es')
    tool = language_tool_python.LanguageTool('es-ES')
    is_bad_rule = lambda rule: rule.message == 'Possible spelling mistake found.' and len(rule.replacements) and rule.replacements[0][0].isupper()
    
    for abstract_data_row in rewritten_spanish_abstracts_file.readlines():
        abstract_data = json.loads(abstract_data_row[:-2])
        abstracts_stats = {
			"Idus_URL": abstract_data["Idus_URL"],
			"id": abstract_data["id"],
			"Resumen": {},
			"Resumen_ChatGPT": {}
		}
        
        original_abstract = abstract_data["Resumen"]
        
        matches = tool.check(original_abstract)    
        matches = [rule for rule in matches if not is_bad_rule(rule)]
        corrected_abstract = \
            language_tool_python.utils.correct(original_abstract, matches)
        print(corrected_abstract)
        
        # just_spaces_original_abstract = original_abstract
        # for mark in PUNCTUATION_MARKS:
        #     just_spaces_original_abstract = \
        #         just_spaces_original_abstract.replace(mark, " ")
        
        # original_abstract_words = just_spaces_original_abstract.split()
        # print(original_abstract_words)
                
        # misspelled = checker.unknown(original_abstract_words)
        # print(misspelled, "\n\n")
        # for word in misspelled:
        #     print(checker.correction(word))
            
        break
    
    tool.close()
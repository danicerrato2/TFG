import json
import language_tool_python

DOCUMENTS_PATH = "documents/"
REWRITTEN_SPANISH_ABSTRACTS_FILENAME = "rewritten_spanish_abstracts.txt"
REWRITTEN_SPANISH_ABSTRACTS_STATS_FILENAME = "rewritten_spanish_abstracts_stats.txt"

PUNCTUATION_MARKS = [',', '.', ';', ':', '-']
IS_BAD_RULE = lambda rule: \
    rule.message == 'Possible spelling mistake found.'\
    and len(rule.replacements)\
    and rule.replacements[0][0].isupper()

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
    tool = language_tool_python.LanguageTool('es-ES')
    
    for abstract_data_row in rewritten_spanish_abstracts_file.readlines():
        try:
            errorCode = 0
            abstract_data = json.loads(abstract_data_row[:-2])
            abstracts_stats = {
				"Idus_URL": abstract_data["Idus_URL"],
				"id": abstract_data["id"],
				"Resumen": {},
				"Resumen_ChatGPT": {}
			}
            
            errorCode = 1
            # Preparando variables que necesitaremos
            original_abstract = abstract_data["Resumen"].lower()
            chatGPT_abstract = abstract_data["Resumen_ChatGPT"].lower()
            
            original_abstract_len = len(original_abstract)
            chatGPT_abstract_len = len(chatGPT_abstract)
            
            just_spaces_original_abstract = original_abstract
            just_spaces_chatGPT_abstract = chatGPT_abstract
            for mark in PUNCTUATION_MARKS:
                just_spaces_original_abstract = \
                    just_spaces_original_abstract.replace(mark, " ")
                just_spaces_chatGPT_abstract = \
                    just_spaces_chatGPT_abstract.replace(mark, " ")
                    
            original_abstract_words = just_spaces_original_abstract.split()
            chatGPT_abstract_words = just_spaces_chatGPT_abstract.split()
            
            original_sentences = original_abstract.split('.')
            chatGPT_sentences = chatGPT_abstract.split('.')
            
            just_spaces_original_sentences = []
            for sentence in original_sentences:
                for mark in PUNCTUATION_MARKS:
                    sentence = sentence.replace(mark, " ")
                if sentence != "":
                    just_spaces_original_sentences.append(sentence)
                    
            just_spaces_chatGPT_sentences = []
            for sentence in chatGPT_sentences:
                for mark in PUNCTUATION_MARKS:
                    sentence = sentence.replace(mark, " ")
                if sentence != "":
                    just_spaces_chatGPT_sentences.append(sentence)
            
            # Correciones
            matches = tool.check(original_abstract)
            matches = [rule for rule in matches if not IS_BAD_RULE(rule)]
            corrected_original_abstract = \
                language_tool_python.utils.correct(
                    original_abstract,
                    matches
                ).lower()
                
            matches = tool.check(chatGPT_abstract)
            matches = [rule for rule in matches if not IS_BAD_RULE(rule)]
            corrected_chatGPT_abstract = \
                language_tool_python.utils.correct(
                    chatGPT_abstract,
                    matches
                ).lower()
            
            just_spaces_corrected_original_abstract = \
                corrected_original_abstract
            just_spaces_corrected_chatGPT_abstract = \
                corrected_chatGPT_abstract
            for mark in PUNCTUATION_MARKS:
                just_spaces_original_abstract = \
                    just_spaces_original_abstract.replace(mark, " ")
                just_spaces_chatGPT_abstract = \
                    just_spaces_chatGPT_abstract.replace(mark, " ")
                    
            original_abstract_words = just_spaces_original_abstract.split()
            chatGPT_abstract_words = just_spaces_chatGPT_abstract.split()
            
            original_sentences = original_abstract.split('.')
            chatGPT_sentences = chatGPT_abstract.split('.')
            
            just_spaces_original_sentences = []
            for sentence in original_sentences:
                for mark in PUNCTUATION_MARKS:
                    sentence = sentence.replace(mark, " ")
                if sentence != "":
                    just_spaces_original_sentences.append(sentence)
                    
            just_spaces_chatGPT_sentences = []
            for sentence in chatGPT_sentences:
                for mark in PUNCTUATION_MARKS:
                    sentence = sentence.replace(mark, " ")
                if sentence != "":
                    just_spaces_chatGPT_sentences.append(sentence)
            
            errorCode = 2
            # Mediciones sobre palabras
            abstracts_stats["Resumen"]["Palabras"] = {}
            abstracts_stats["Resumen_ChatGPT"]["Palabras"] = {}
            
            abstracts_stats["Resumen"]["Palabras"]["Cantidad"] = \
                len(original_abstract_words)
            abstracts_stats["Resumen_ChatGPT"]["Palabras"]["Cantidad"] = \
                len(chatGPT_abstract_words)
                
            abstracts_stats["Resumen"]["Palabras"]["Num_Distintas"] = \
                len(set(original_abstract_words))
            abstracts_stats["Resumen_ChatGPT"]["Palabras"]["Num_Distintas"] = \
                len(set(chatGPT_abstract_words))
            
            errorCode = 3
            # Mediciones sobre signos de puntuacion    
            abstracts_stats["Resumen"]["Signos"] = {}
            abstracts_stats["Resumen_ChatGPT"]["Signos"] = {}
            
            for mark in PUNCTUATION_MARKS:
                abstracts_stats["Resumen"]["Signos"][mark] = \
                    original_abstract.count(mark) / original_abstract_len
                abstracts_stats["Resumen_ChatGPT"]["Signos"][mark] = \
                    chatGPT_abstract.count(mark) / chatGPT_abstract_len
            
            errorCode = 4
            # Mediciones sobre frases
            abstracts_stats["Resumen"]["Frases"] = {}
            abstracts_stats["Resumen_ChatGPT"]["Frases"] = {}
            
            abstracts_stats["Resumen"]["Frases"]["Cantidad"] = \
                len(original_sentences) / original_abstract_len
            abstracts_stats["Resumen_ChatGPT"]["Frases"]["Cantidad"] = \
                len(chatGPT_sentences) / chatGPT_abstract_len
                
            abstracts_stats["Resumen"]["Frases"]["Num_Palabras"] = []
            abstracts_stats["Resumen"]["Frases"]["Num_Caracteres"] = []
            abstracts_stats["Resumen_ChatGPT"]["Frases"]["Num_Palabras"] = []
            abstracts_stats["Resumen_ChatGPT"]["Frases"]["Num_Caracteres"] = []
            
            for sentence in just_spaces_original_sentences:
                abstracts_stats["Resumen"]["Frases"]["Num_Palabras"]\
                    .append(len(sentence.split()) / len(original_abstract_words))
                abstracts_stats["Resumen"]["Frases"]["Num_Caracteres"]\
                    .append(len(sentence) / original_abstract_len)
            
            for sentence in just_spaces_chatGPT_sentences:
                abstracts_stats["Resumen_ChatGPT"]["Frases"]["Num_Palabras"]\
                    .append(len(sentence.split()) / len(chatGPT_abstract_words))
                abstracts_stats["Resumen_ChatGPT"]["Frases"]["Num_Caracteres"]\
                    .append(len(sentence) / chatGPT_abstract_len)
                    
            errorCode = 5
            rewritten_spanish_abstracts_stats_file.write(
				f"{str(abstracts_stats)},\n"
    		)
        
        except Exception as exception:
            print("Error en", abstract_data["Idus_URL"], f" - ErrorCode {errorCode}\n{exception}")
            continue
    
    rewritten_spanish_abstracts_file.close()
    rewritten_spanish_abstracts_stats_file.close()
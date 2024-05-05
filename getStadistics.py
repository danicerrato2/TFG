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

def get_text_words(text):
    for mark in PUNCTUATION_MARKS:
        text = text.replace(mark, " ")

    return text.split()

def get_text_just_spaces_sentences(sentences):
    just_spaces_sentences = []
    for sentence in sentences:
        for mark in PUNCTUATION_MARKS:
            sentence = sentence.replace(mark, " ")
        if sentence != "":
            just_spaces_sentences.append(sentence)
    
    return just_spaces_sentences

def get_corrected_text(text):
    matches = tool.check(text)
    matches = [rule for rule in matches if not IS_BAD_RULE(rule)]
    corrected_text = language_tool_python.utils.correct(text, matches).lower()
    
    return corrected_text, len(matches)

def get_words_stats(words, corrected_words):
    words_stats = {}
    num_words = len(words)
    
    words_stats["Cantidad"] = num_words
    words_stats["Num_Distintas"] = len(set(words))
    num_corrections = 0
    for word in words:
        if corrected_words.count(word) == 0:
            num_corrections += 1
    words_stats["Num_Corregidas"] = num_corrections / num_words
    
    return words_stats

def get_marks_stats(text):
    mark_stats = {}
    text_len = len(text)
    
    for mark in PUNCTUATION_MARKS:
        mark_stats[mark] = text.count(mark) / text_len
        
    return mark_stats

def get_sentences_stats(text_sentences, text_len, num_text_words):
    sentences_stats = {}
    sentences_stats["Num_Palabras"] = []
    sentences_stats["Num_Caracteres"] = []
    
    sentences_stats["Cantidad"] = len(text_sentences) / text_len
    for sentence in get_text_just_spaces_sentences(text_sentences):
        sentences_stats["Num_Palabras"].append(len(sentence.split()) / num_text_words)
        sentences_stats["Num_Caracteres"].append(len(sentence) / text_len)
        
    return sentences_stats

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

            # Preparando variables que necesitaremos
            errorCode = 1
            original_abstract = abstract_data["Resumen"].lower()
            chatGPT_abstract = abstract_data["Resumen_ChatGPT"].lower()

            original_abstract_words = get_text_words(original_abstract)
            chatGPT_abstract_words = get_text_words(chatGPT_abstract)

            original_sentences = original_abstract.split('.')
            chatGPT_sentences = chatGPT_abstract.split('.')

            corrected_original_abstract, num_original_corrections = \
                get_corrected_text(original_abstract)
            corrected_chatGPT_abstract, num_chatGPT_corrections = \
                get_corrected_text(chatGPT_abstract)

            corrected_original_abstract_words = get_text_words(corrected_original_abstract)
            corrected_chatGPT_abstract_words = get_text_words(corrected_chatGPT_abstract)                    

            # Mediciones sobre palabras
            errorCode = 2
            abstracts_stats["Resumen"]["Palabras"] = get_words_stats(
                original_abstract_words,
                corrected_original_abstract_words)
            abstracts_stats["Resumen_ChatGPT"]["Palabras"] = get_words_stats(
                chatGPT_abstract_words,
                corrected_chatGPT_abstract_words)

            # Mediciones sobre signos de puntuacion
            errorCode = 3
            abstracts_stats["Resumen"]["Signos"] = get_marks_stats(original_abstract)
            abstracts_stats["Resumen_ChatGPT"]["Signos"] = get_marks_stats(chatGPT_abstract)

            # Mediciones sobre frases
            errorCode = 4
            abstracts_stats["Resumen"]["Frases"] = get_sentences_stats(
                original_sentences,
                len(original_abstract),
                len(original_abstract_words))
            abstracts_stats["Resumen_ChatGPT"]["Frases"] = get_sentences_stats(
                chatGPT_sentences,
                len(chatGPT_abstract),
                len(chatGPT_abstract_words))

            # Guardar informacion
            errorCode = 5
            rewritten_spanish_abstracts_stats_file.write(
				f"{str(abstracts_stats)},\n"
    		)

        except Exception as exception:
            print("Error en", abstract_data["Idus_URL"], f" - ErrorCode {errorCode}\n{exception}")
            continue

    rewritten_spanish_abstracts_file.close()
    rewritten_spanish_abstracts_stats_file.close()
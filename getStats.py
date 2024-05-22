import json
import language_tool_python
import nltk
import string

DOCUMENTS_PATH = "documents/"
REWRITTEN_SPANISH_ABSTRACTS_FILENAME = "rewritten_spanish_abstracts.txt"
SPANISH_ABSTRACTS_STATS_FILENAME = "spanish_abstracts_stats.txt"
SPANISH_ORIGINAL_WORDS_FILE = "spanish_original_words.txt"
SPANISH_CHATGPT_WORDS_FILE = "spanish_chatgpt_words.txt"

IS_BAD_RULE = lambda rule: \
    rule.message == 'Possible spelling mistake found.'\
    and len(rule.replacements)\
    and rule.replacements[0][0].isupper()

rewritten_spanish_abstracts_file = open(
    DOCUMENTS_PATH + REWRITTEN_SPANISH_ABSTRACTS_FILENAME,
    "r",
    encoding='utf-8'
)

spanish_abstracts_stats_file = open(
    DOCUMENTS_PATH + SPANISH_ABSTRACTS_STATS_FILENAME,
    "a",
    encoding='utf-8'
)

spanish_original_words_file = open(
    DOCUMENTS_PATH + SPANISH_ORIGINAL_WORDS_FILE,
    "a",
    encoding='utf-8'
)

spanish_chatGPT_words_file = open(
    DOCUMENTS_PATH + SPANISH_CHATGPT_WORDS_FILE,
    "a",
    encoding='utf-8'
)

original_used_words = {}
chat_GPT_used_words = {}

tool = language_tool_python.LanguageTool('es-ES')

###
# Downloads the necessary resources of 'nltk' library
###
def download_nltk_resources():
    nltk.download('tagsets')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')

###
# Separates the text into meaningful words, meaningless words and punctuation marks
###
def separate_text(text):
    stop_words = set(nltk.corpus.stopwords.words('spanish'))
    cleaned_words = []
    punctuation_marks = []
    stop_words = []
    
    for token in nltk.word_tokenize(text):
        if token in stop_words:
            stop_words.append(token)
        elif token in string.punctuation:
            punctuation_marks.append(token)
        else:
            cleaned_words.append(token)
            
    return cleaned_words, stop_words, punctuation_marks

###
# Gets the grammar group of the grammar type
###
def get_grammar_group(tag: str):
    match tag:
        case "WRB" | "RB" | "RBS" | "RBR":
            return "Adverbios"
        case "WP$" | "WP" | "PRP$" | "PRP":
            return "Pronombres"
        case "WDT" | "PDT" | "DT":
            return "Determinantes"
        case "VBZ" | "VBP" | "VBN" | "VBG" | "VBD" | "VB":
            return "Verbos"
        case "NNS" | "NNP" | "NN" | "NNPS":
            return "Nombres"
        case "JJS" | "JJR" |"JJ":
            return "Adjetivos"
        case "LS":
            return "Listado"
        case "IN":
            return "Preposiciones"
        case "CD":
            return "Numeros"
        case "SYM":
            return "Simbolo"
        case ",":
            return "Coma"
        case ".":
            return "Final"
        case ":":
            return "Elipsis"
        case _:
            return "Otros"

###
# Gets the word grammar types appearances
###
def get_grammar_types_count(words, num_words):
    grammar_types = {
        "Adverbios": 0,
        "Pronombres": 0,
        "Determinantes": 0,
        "Verbos": 0,
        "Nombres": 0,
        "Adjetivos": 0,
        "Listado": 0,
        "Preposiciones": 0,
        "Numeros": 0,
        "Simbolo": 0,
        "Coma": 0,
        "Final": 0,
        "Elipsis": 0,
        "Otros": 0
    }
    
    for _, tag in nltk.pos_tag(words):
        tag_group = get_grammar_group(tag)
        grammar_types[tag_group] += 1    
            
    for grammar_type in grammar_types.keys():
        grammar_types[grammar_type] /= num_words

    return grammar_types

###
# Gets words stats
###
def get_words_stats(cleaned_words, stop_words):
    words_stats = {}
    
    num_cleaned_words = len(cleaned_words)
    num_stop_words = len(stop_words)
    num_words = num_cleaned_words + num_stop_words
    
    words_stats["Num_Palabras"] = num_words
    words_stats["Num_Palabras_Distintas"] = len(set(cleaned_words)) / num_words
    words_stats["Tipos"] = get_grammar_types_count(cleaned_words, num_words)
    
    return words_stats

###
# Gets the number of corrections using 'LanguageTool' of 'language_tool_python' library
###
def get_num_corrections(text):
    global tool
    matches = tool.check(text)
    matches = [rule for rule in matches if not IS_BAD_RULE(rule)]
    
    return len(matches)

###
# Gets marks stats
###
def get_marks_stats(punctuation_marks, text_len):
    marks_stats = {}    
    
    marks_stats["Num_Signos"] = len(punctuation_marks) / text_len
        
    return marks_stats

###
# Gets senteces stats
###
def get_sentences_stats(text, num_text_words):
    sentences_stats = {}
    sentences_stats["Num_Palabras_Frase"] = []
    sentences_stats["Num_Palabras_Frase_Norm"] = []
    sentences_stats["Num_Caracteres_Frase"] = []
    
    text_len = len(text)
    sentences = nltk.sent_tokenize(text)
    num_sentences = len(sentences)
    
    sentences_stats["Num_Frases"] = num_sentences
    sentences_stats["Num_Frases_Norm"] = num_sentences / num_text_words
    for sentence in sentences:
        num_sentence_words = len(nltk.word_tokenize(sentence))
        sentences_stats["Num_Caracteres_Frase"].append(len(sentence) / text_len)
        sentences_stats["Num_Palabras_Frase"].append(num_sentence_words)
        sentences_stats["Num_Palabras_Frase_Norm"].append(num_sentence_words / num_text_words)
        
    return sentences_stats 

###
# Gets all the stats
###
def get_stats(text, text_type):
    stats = {}
    error_code = 0
    
    try:
        cleaned_words, stop_words, punctuation_marks = separate_text(text)
        num_words = len(cleaned_words) + len(stop_words)
        
        error_code = 1
        stats["Num_Caracteres"] = len(text)
        
        error_code = 2
        stats["Palabras"] = get_words_stats(cleaned_words, stop_words)
        
        error_code = 3
        stats["Palabras"]["Correcciones"] = get_num_corrections(text) / num_words
        
        error_code = 4
        stats["Signos"] = get_marks_stats(punctuation_marks, stats["Num_Caracteres"])
        
        error_code = 5
        stats["Frases"] = get_sentences_stats(text, num_words)
        
        if text_type == "original":
            global spanish_original_words_file
            spanish_original_words_file.write(" ".join(cleaned_words) + " ")
        else:
            global spanish_chatGPT_words_file
            spanish_chatGPT_words_file.write(" ".join(cleaned_words) + " ")

    except Exception as exception:
        print(f"ErrorCode ({error_code})\n{exception}")
        raise Exception(f"ErrorCode ({error_code})\n{exception}")
         
    return stats

if __name__ == '__main__':    
    download_nltk_resources()

    abstract_data_rows = rewritten_spanish_abstracts_file.readlines()
    rewritten_spanish_abstracts_file.close()
    num_abstracts = len(abstract_data_rows)
    
    for i, abstract_data_row in enumerate(abstract_data_rows):        
        print(f"Abstract {i + 1} ({round(((i + 1) / num_abstracts) * 100, 2)}%)")
        try:
            abstract_data = json.loads(abstract_data_row[:-2])
            abstract_stats = {
                "Idus_URL": abstract_data["Idus_URL"],
                "id": abstract_data["id"],
                "Resumen": {},
                "Resumen_ChatGPT": {}
            }

            original_abstract = abstract_data["Resumen"].lower()
            chatGPT_abstract = abstract_data["Resumen_ChatGPT"].lower()

            print("Getting stats...")
            abstract_stats["Resumen"] = get_stats(original_abstract, "original")
            abstract_stats["Resumen_ChatGPT"] = get_stats(chatGPT_abstract, "chat_GPT")

            print("Saving stats...")
            spanish_abstracts_stats_file.write(f"{str(abstract_stats)},\n")
            
            print("Stats saved")
            
        except Exception as exception:
            print(f"Error en abstract {i}\n{exception}")


    spanish_abstracts_stats_file.close()
    spanish_original_words_file.close()
    spanish_chatGPT_words_file.close()
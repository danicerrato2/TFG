import json
import language_tool_python
import nltk
import string

DOCUMENTS_PATH = "documents/"
REWRITTEN_SPANISH_ABSTRACTS_FILENAME = "rewritten_spanish_abstracts.txt"
SPANISH_ABSTRACTS_STATS_FILENAME = "spanish_abstracts_stats.txt"
SPANISH_ORIGINAL_WORDS_FILE = "spanish_original_words.txt"
SPANISH_CHATGPT_WORDS_FILE = "spanish_chatgpt_words.txt"
ERROR_LOG_FILE = "error.log"

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

error_log_file = open(ERROR_LOG_FILE, "a", encoding='utf-8')

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
# Gets the word grammar types appearances
###
def get_grammar_types_count(words, num_words):
    grammar_types = {}
    tags = []
    
    for _, tag in nltk.pos_tag(words):
        if tag not in tags:
            tags.append(tag)
            grammar_types[tag] = 1
        else:
            grammar_types[tag] += 1    
            
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
    words_stats["Num_Importantes"] = num_cleaned_words / num_words
    words_stats["Num_No_Importantes"] = num_stop_words / num_words
    words_stats["Num_Importates_Distintas"] = len(set(cleaned_words)) / num_cleaned_words
    words_stats["Tipos"] = get_grammar_types_count(cleaned_words, num_cleaned_words)
    
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
    for mark in string.punctuation:
        marks_stats[mark] = punctuation_marks.count(mark) / text_len
        
    return marks_stats

###
# Gets senteces stats
###
def get_sentences_stats(text, num_text_words):
    sentences_stats = {}
    sentences_stats["Num_Palabras"] = []
    sentences_stats["Num_Caracteres"] = []
    
    text_len = len(text)
    sentences = nltk.sent_tokenize(text)
    
    sentences_stats["Num_Frases"] = len(sentences) / text_len
    for sentence in sentences:
        sentences_stats["Num_Caracteres"].append(len(sentence) / text_len)
        sentences_stats["Num_Palabras"].append(len(nltk.word_tokenize(sentence)) / num_text_words)
        
    return sentences_stats

###
# Add words list appearances into the global words appearances
###
def add_words_appearances(words, used_words):
    for word in words:
        try:
            used_words[word] += 1
        except Exception:
            used_words[word] = 1
    
    return used_words      

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
        stats["Longitud"] = len(text)
        
        error_code = 2
        stats["Palabras"] = get_words_stats(cleaned_words, stop_words)
        
        error_code = 3
        stats["Palabras"]["Correcciones"] = get_num_corrections(text) / num_words
        
        error_code = 4
        stats["Signos"] = get_marks_stats(punctuation_marks, stats["Longitud"])
        
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
    last_abstract = 741
    
    download_nltk_resources()

    abstract_data_rows = rewritten_spanish_abstracts_file.readlines()
    rewritten_spanish_abstracts_file.close()
    num_abstracts = len(abstract_data_rows)
    
    for i, abstract_data_row in enumerate(abstract_data_rows):

        if i < last_abstract:
            continue
        
        if final_abstract < i:
            break
        
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
            error_log_file.write(f"Error en abstract {i}\n{exception}")

    error_log_file.close()
    spanish_abstracts_stats_file.close()
    spanish_original_words_file.close()
    spanish_chatGPT_words_file.close()
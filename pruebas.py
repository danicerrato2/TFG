import json
import nltk
import string

DOCUMENTS_PATH = "documents/"
REWRITTEN_SPANISH_ABSTRACTS_FILENAME = "rewritten_spanish_abstracts.txt"
REWRITTEN_SPANISH_ABSTRACTS_STATS_FILENAME = "rewritten_spanish_abstracts_stats.txt"

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

def download_resources():
    nltk.download('tagsets')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')

def clean_text(text):
    stop_words = set(nltk.corpus.stopwords.words('spanish'))
    cleaned_words = []
    for word in nltk.word_tokenize(text):
        word = word.lower()
        if word not in stop_words and word not in string.punctuation:
            cleaned_words.append(word)
            
    return cleaned_words

if __name__ == '__main__':
    nltk.help.upenn_tagset()

    # download_resources()
    
    # for abstract_data_row in rewritten_spanish_abstracts_file.readlines():
    #     abstract_data = json.loads(abstract_data_row[:-2])
    #     abstracts_stats = {
	# 		"Idus_URL": abstract_data["Idus_URL"],
	# 		"id": abstract_data["id"],
	# 		"Resumen": {},
	# 		"Resumen_ChatGPT": {}
	# 	}
        
    #     original_abstract = abstract_data["Resumen"]
        
        
    #     tokens = nltk.word_tokenize(original_abstract)
    #     sentences = nltk.sent_tokenize(original_abstract)
    #     cleaned_text = clean_text(original_abstract)

    #     print(sentences)

        # freqs = nltk.FreqDist(tokens)
        # print(freqs)        
            
        # break
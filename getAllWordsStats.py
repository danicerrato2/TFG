import nltk

if __name__ == '__main__':
    original_words_file = open("documents/spanish_original_words.txt", "r", encoding="utf-8")
    chatGPT_words_file = open("documents/spanish_chatgpt_words.txt", "r", encoding="utf-8")
    
    print(nltk.help.upenn_tagset())
    
    original_words_file.close()
    chatGPT_words_file.close()
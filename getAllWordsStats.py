NUM_ABSTRACTS = 1447

def get_words_count(file):
    words_count = {}
    
    for word in file.read().split():
        try:
            words_count[word] += 1
        except Exception:
            words_count[word] = 1
            
    for word in words_count.keys():
        words_count[word] /= NUM_ABSTRACTS
    
    return words_count
    
if __name__ == '__main__':
    original_words_file = open("documents/spanish_original_words.txt", "r", encoding="utf-8")
    chatGPT_words_file = open("documents/spanish_chatgpt_words.txt", "r", encoding="utf-8")
    stats_file = open("documents/spanish_abstracts_stats.txt", "a", encoding="utf-8")
    
    words_count = {}
    words_count["Resumen"] = get_words_count(original_words_file)
    words_count["Resumen_ChatGPT"] = get_words_count(chatGPT_words_file)
    
    stats_file.write(f"{str(words_count)},\n")
    
    stats_file.close()
    original_words_file.close()
    chatGPT_words_file.close()
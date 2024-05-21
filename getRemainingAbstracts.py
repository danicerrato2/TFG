import json

def get_IdusURL(data: str):
    data = data.split("\"Idus_URL\":")[1]
    data = data.split(",")[0]
    data = data.split("\"")[1]
    
    return data

if __name__ == '__main__':
    stats_file = open("documents/spanish_abstracts_stats.txt", "r", encoding='utf-8')
    rewritten_abstracts_file = open("documents/rewritten_spanish_abstracts.txt", "r", encoding="utf-8")
    recovered_abstracts_file = open("recovered_abstracts.txt", "a", encoding='utf-8')
    
    stats_rows = stats_file.readlines()
    stats_file.close()
    abstracts_rows = rewritten_abstracts_file.readlines()
    rewritten_abstracts_file.close()
    
    stats_urls = []
    for i, stats_row in enumerate(stats_rows):
        stats_data = json.loads(stats_row[:-2])
        if stats_data["Idus_URL"] in stats_urls:
            print(stats_data["Idus_URL"])
        stats_urls.append(stats_data["Idus_URL"])
    
    for i, abstract_row in enumerate(abstracts_rows):
        url = get_IdusURL(abstract_row)
        if url not in stats_urls:
            recovered_abstracts_file.write(abstract_row)
    
    recovered_abstracts_file.close()
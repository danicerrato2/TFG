import json

documents_path = "../documents/"
spanish_abstracts_filename = "spanish_abstracts.txt"
rewritten_spanish_abstracts_filename = "rewritten_spanish_abstracts_more3000.txt"

spanish_abstracts_file = open(
    documents_path + spanish_abstracts_filename,
    "r",
    encoding='utf-8'
)

MIN_SIZE = 3000

if __name__ == '__main__':    	
    num_abstracts = 0
    last_abstract = 100
    max_abstracts = 500
    
    for abstract_data_row in spanish_abstracts_file.readlines()[::-1]: 
        
        if len(abstract_data_row) <= MIN_SIZE:
            continue
        
        num_abstracts += 1
        if num_abstracts <= last_abstract:
            continue
        
        input()
        
        abstract_data = json.loads(abstract_data_row[:-2])
        
        print("\n" + abstract_data["Resumen"] + "\n")
        abstract_data["Resumen_ChatGPT"] = ""
        
        with open(
			documents_path + rewritten_spanish_abstracts_filename,
			"a",
			encoding='utf-8'
		) as rewritten_file:
            rewritten_file.write(f"{str(abstract_data)},\n")
    
    spanish_abstracts_file.close()
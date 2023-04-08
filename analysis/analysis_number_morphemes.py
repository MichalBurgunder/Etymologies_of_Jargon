from utils import  find_field_position
from file_management import save_as_csv
from config import file_names

def number_of_morphemes(data, headers, scrape_ident=''):
    no_morph_pos = find_field_position(headers, "Nr. of Morphemes")
    scrape_ident_pos = find_field_position(headers, "Scrape Identifier")
    
    final_data = [[i for i in range(1,10)], [0 for i in range(1,10)]]
    print(final_data)
    errors = []
    for i in range(0, len(data)):
        if data[i][scrape_ident_pos] == scrape_ident or (scrape_ident == 'ALL' and data[i][scrape_ident_pos] != "ADD"):
            try :
                if int(data[i][no_morph_pos]) < 10:
                    final_data[1][int(data[i][no_morph_pos])-1] += 1
            except:
                errors.append(f"Warning: Morpheme entry \"{data[i][no_morph_pos]}\", scrape identifier {data[i][scrape_ident_pos]} must be an integer less than 10")
    
    if len(errors):
        for err in errors:
            print(err)
        print("Fix these errors before continuing.")
        exit()
    
    postfix = scrape_ident if scrape_ident != '' else "ALL"
    save_as_csv(final_data, file_names["morpheme"] + postfix)
    return
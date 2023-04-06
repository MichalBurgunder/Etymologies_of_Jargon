from utils import  find_field_position
from file_management import save_as_csv


def number_of_morphemes(data, headers, scrape_ident=''):
    no_morph_pos = find_field_position(headers, "Nr. of Morphemes")
    scrape_ident_pos = find_field_position(headers, "Scrape Identifier")
    
    hash_table = {}
    
    for i in range(0, len(data)):
        if scrape_ident == '' or data[i][scrape_ident_pos] == scrape_ident:
            if data[i][no_morph_pos] not in hash_table:
                hash_table[data[i][no_morph_pos]] = 1
            else:
                hash_table[data[i][no_morph_pos]] += 1
            
    number = hash_table.keys()
    frequency = hash_table.values()
    
    postfix = scrape_ident if scrape_ident != '' else "ALL"
    save_as_csv([number, frequency], "number_morphemes_" + postfix)
    return
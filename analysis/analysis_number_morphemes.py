from utils import  find_field_position
from config import file_names, top_languages
from file_management import save_as_csv

def number_of_morphemes(data, headers, scrape_ident=''):
    """
    Extracts the number of morphemes from a given data set (scrape  identifier)
    and saves easily graphable results into a .csv file
    """
    no_morph_pos = find_field_position(headers, "Nr. of Morphemes")
    scrape_ident_pos = find_field_position(headers, "Scrape Identifier")
    scrape_clean_pos = find_field_position(headers, "Cleaned Name")
    
    # max. number of morphemes
    mm = 10
    # counting number of morphemes
    final_data = [[i for i in range(1,mm)], [0 for i in range(1,mm)]]

    errors = []
    for i in range(0, len(data)):
        if (
                (data[i][scrape_ident_pos] == scrape_ident) or # taking only from 1 data set
                (scrape_ident == 'ALL' and data[i][scrape_ident_pos] != "ADD") or # taking from all sets except for additives
                (scrape_ident == 'TOP' and data[i][scrape_clean_pos].lower() in top_languages) # taking only those fields that are within a specific array of strings
        ):
            try:
                # number of mophemes cannot exceed 10. Used to verify the
                # correctness of the field. Increase if necessary
                if int(data[i][no_morph_pos]) < mm: 
                    final_data[1][int(data[i][no_morph_pos])-1] += 1
            except:
                print(data[i][scrape_clean_pos])
                errors.append(f"Warning: Morpheme entry \"{data[i][no_morph_pos]}\", scrape identifier {data[i][scrape_ident_pos]} must be an integer less than 10")
    
    if len(errors):
        for err in errors:
            print(err)
        print("Fix these errors before continuing.")
        exit()
    
    postfix = scrape_ident if scrape_ident != '' else "ALL"
    save_as_csv(final_data, file_names["morpheme"] + postfix)
    return
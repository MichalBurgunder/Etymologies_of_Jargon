
from utils import  find_field_position, clean_scrape_name
from file_management import save_as_csv

def prepare_jargon_length(data, headers, scrape_ident=''):
    """
    Collects all data necessary to analyze and graph the length of jargons (Cleaned Name). 
    It saves the data into a name_length.csv
    """
    print("starting jargon length analysis...")
    clean_name_pos = find_field_position(headers, 'Cleaned Name')
    scarpe_ident_pos = find_field_position(headers, 'Scrape Identifier')

    the_max = max([len(line[clean_name_pos]) for line in data])
    final_data = [0] * (the_max+1)

    for i in range(0, len(data)):
        if scrape_ident == '' or data[i][scarpe_ident_pos] == scrape_ident:
            final_data[len(data[i][clean_name_pos])] += 1
    
    cleaned_scrape_name = clean_scrape_name(scrape_ident)
    save_as_csv([[i for i in range(0, the_max)], final_data], f'name_length_{cleaned_scrape_name}')
    return
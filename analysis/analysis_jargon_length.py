
from utils import  find_field_position, clean_scrape_name
from file_management import save_as_csv


def remove_specification(name):
    """
    Given that certain data points' Cleaned Name field specify the data set,
    this function removes this specification to get the actual name, instead of
    the one used during deduplication
    """
    
    the_range = [None, None]
    edge = 1
    # we go backwards, in case a name for some reason uses brackets otherwise, if later on
    # brackets are added at the end for every name (for standardize deduplication), this
    # ensures that the complexity of this function is minimal
    for i in range(len(name)-1, 0, -1): 
        if edge and name[i] == ")":
            the_range[edge] = i
            edge = 0
        elif not edge and name[i] == "(":
            the_range[edge] = i
            break
    if not the_range[0]:
        raise Exception("Bracket was closed, but never opened. Incorrect cleaned name?")
    return name[0:the_range[0]-1]

def prepare_jargon_length(data, headers, scrape_ident=''):
    """
    Collects all data necessary to analyze and graph the length of jargons
    (Cleaned Name). It saves the data into a name_length.csv
    """
    print("starting jargon length analysis...")
    
    clean_name_pos = find_field_position(headers, 'Cleaned Name')
    scarpe_ident_pos = find_field_position(headers, 'Scrape Identifier')

    the_max = max([len(remove_specification(line[clean_name_pos])) for line in data])
    final_data = [0] * (the_max+1)

    for i in range(0, len(data)):
        if scrape_ident == '' or data[i][scarpe_ident_pos] == scrape_ident:
            final_data[len(data[i][clean_name_pos])] += 1
    
    cleaned_scrape_name = clean_scrape_name(scrape_ident)
    save_as_csv([[i for i in range(0, the_max)], final_data], f'name_length_{cleaned_scrape_name}')
    return

# name = "julia (programming lang)"
# print(remove_specification(name))
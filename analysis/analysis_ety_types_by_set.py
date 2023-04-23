import numpy as np
from utils import find_field_position
from file_management import save_as_csv

def make_into_csv(data):
    final_data = [data[0], data[1]]
    
    for i in range(0, len(data[2])):
        final_data.append(data[2][i])
    return final_data

def prepare_ety_type_counts(data, headers, data_set_names):
    """
    Counts the ety types of a given set of data sets and saves them 
    """
    second_ety_type_pos = find_field_position(headers, '2nd Ety. type')
    all_categories_set = set(np.array(data)[:,second_ety_type_pos])
    all_categories = [the_category for the_category in all_categories_set]

    final_data = np.zeros((len(data_set_names), len(all_categories)), dtype=int)
    
    cat_to_pos = {}
    ident_to_pos = {}
    for i in range(0, len(data_set_names)):
        ident_to_pos[data_set_names[i]] = i
    
    for i in range(0, len(all_categories)):
        cat_to_pos[all_categories[i]] = i

    scarpe_ident_pos = find_field_position(headers, 'Scrape Identifier')
    
    for i in range(0, len(data)):
        # to remove any odd additions
        if data[i][scarpe_ident_pos] in data_set_names:
            final_data[ident_to_pos[data[i][scarpe_ident_pos]]][cat_to_pos[data[i][second_ety_type_pos]]] += 1
    
    # replace the empty string to "Missing"
    all_categories = [category if category != '' else "Missing" for category in all_categories]
    
    saved_data = [data_set_names]
    [saved_data.append(data)]
    save_as_csv(make_into_csv([data_set_names, all_categories, final_data]), "ety_types_by_data_set")
    return 


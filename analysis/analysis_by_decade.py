
import numpy as np    # to create dummy data
from config import find_field_position
from utils import number_only, fill_no_etymology, print_errors
from file_management import save_as_csv

def remove_special_chars_year(all_elements, headers):
    """
    For the "Year" field, it makes sure that the field will always be an integer.
    If it isn't it tries to give a best estimate of what year was meant.
    """
    year_pos = find_field_position(headers, "Year")
    si_pos = find_field_position(headers, "Scrape Identifier")
    cn_pos = find_field_position(headers, "Cleaned Name")
    
    errors = []
    
    for i in range(0,len(all_elements)):
        if  all_elements[i][year_pos] == '':
             all_elements[i][year_pos] = "0"
        try:
            the_num = int(number_only(str(all_elements[i][year_pos])))
            all_elements[i][year_pos] = the_num
        except:
            errors.append(f"Warning: Entry {all_elements[i][cn_pos]} (Scrape Identifier: {all_elements[i][si_pos]}) has an invalid year")
    if len(errors):
        print_errors(errors)
        exit()


def get_all_unique_etymology_types(all_elements, headers, scrape_ident='',type="Ety. Type"):
    """
    Get's all the different strings that are present in the "Ety. type" field of our data.
    """
    etytype_pos = find_field_position(headers, type)
    scrape_ident_pos = find_field_position(headers, "Scrape Identifier")
    ety_types = {}
    ety_types_arr = []
    for i in range(0,len(all_elements)):
        if (all_elements[i][scrape_ident_pos] == scrape_ident or scrape_ident == '') and all_elements[i][etytype_pos] not in ety_types:
            ety_types[all_elements[i][etytype_pos]] = True
            ety_types_arr.append(all_elements[i][etytype_pos])
    return ety_types_arr

def get_column_hash_table():
    """
    A preprocessing step that gives back an appropriate hash table with which we can count instances of a given string.
    """
    hash_table = {}
    # in order to track ety types by year, we set the numbers to go from 1900 to 2030. 
    # this way, to get the years, we simply need to mulitiply by 10.
    for i in range(190,203,1):
        hash_table[i] = i-190
    return hash_table
    
def prepare_year_type_data(all_elements, headers, scrape_ident, ety_type):
    """
    Prepares all of the data necessary to analyze and graph the etymological types by year.
    """
    print("starting ety. type by year analysis...")
    separation = 10
    columns = [f'{i}-{i+10}' for i in range(1900, 2030, separation)]

    hash_table_columns = get_column_hash_table() # sets the years, so that one can query it
    year_pos = find_field_position(headers, "Year")
    ety_type_pos = find_field_position(headers, ety_type)
    scrape_ident_pos = find_field_position(headers, "Scrape Identifier")
    data = []

    rows_names = []
    
    for i in range(0, len(all_elements)):
        # to remove machine code, which has technically first been created in 1804
        if all_elements[i][year_pos] < 1900:
            continue
        # only doing the analysis on one dataset (programming languages)
        if all_elements[i][scrape_ident_pos] != scrape_ident:
            continue
        
        col_pos = hash_table_columns[int(np.floor(all_elements[i][year_pos]/10))]
        
        row_pos = None
        if all_elements[i][ety_type_pos] not in rows_names:
            rows_names.append(all_elements[i][ety_type_pos])
            data.append([0] * len(columns))
            row_pos = len(rows_names) - 1
        else:
            row_pos = rows_names.index(all_elements[i][ety_type_pos])
        
        data[row_pos][col_pos] += 1
    
    data.insert(0, columns)
    data.append(rows_names)
    return data
    
    
def prepare_ety_by_decade_data(all_elements, headers, scrape_ident='', type=1):
    """
    Extracts from the processed data all "subdata" necessary to analyze ety types by year, and saves this data as a CSV.
    """
    ety_type = "Ety. type" if type == 1 else "2nd Ety. type"
    print("starting ety type by year analysis...")
    remove_special_chars_year(all_elements, headers)
    fill_no_etymology(all_elements, headers, field=ety_type)
    unique_ety_types = get_all_unique_etymology_types(all_elements, headers, scrape_ident, ety_type)
    data = prepare_year_type_data(all_elements, headers, scrape_ident, ety_type)
    save_as_csv(data, f"ety_type_{type}_by_decade")

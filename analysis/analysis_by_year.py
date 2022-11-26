
from config import find_field_position
from utils import number_only, fill_no_etymology
import pandas as pd
from config import root
from file_management import save_as_csv
import matplotlib.pyplot as plt
import numpy as np    # to create dummy data

def remove_special_chars_year(all_elements, headers):
    year_pos = find_field_position(headers, "Year")
    for i in range(0,len(all_elements)):
        if  all_elements[i][year_pos] == '':
             all_elements[i][year_pos] = "0"
        all_elements[i][year_pos] = int(number_only(all_elements[i][year_pos]))
    


def get_all_unique_etymology_types(all_elements, headers):
    etytype_pos = find_field_position(headers, "Ety. type")
    ety_types = {}
    ety_types_arr = []
    for i in range(0,len(all_elements)):
        if all_elements[i][etytype_pos] not in ety_types:
            ety_types[all_elements[i][etytype_pos]] = True
            ety_types_arr.append(all_elements[i][etytype_pos])
    return ety_types_arr

def get_column_hash_table():
    hash_table = {}
    for i in range(190,203,1):
        hash_table[i] = i-190
    return hash_table
    
def prepare_year_type_data(all_elements, headers):
    print("starting ety. type by year anaylsis...")
    separation = 10
    columns = [f'{i}-{i+10}' for i in range(1900, 2030, separation)]
    print(columns)
    hash_table_columns = get_column_hash_table() # sets the years, so that one can query it
    year_pos = find_field_position(headers, "Year")
    ety_type_pos = find_field_position(headers, "Ety. type")
    data = []
    # data.append([0] * len(columns)) # I don't think that this works, no?
    rows_names = []
    
    # print(hash_table_columns)
    # exit()
    for i in range(0, len(all_elements)):
        if all_elements[i][year_pos] < 1900:
            continue
        col_pos = hash_table_columns[int(np.floor(all_elements[i][year_pos]/10))]
        
        row_pos = None
        if all_elements[i][ety_type_pos] not in rows_names:
            rows_names.append(all_elements[i][ety_type_pos])
            data.append([0] * len(columns))
            row_pos = len(rows_names) - 1
        else:
            row_pos = rows_names.index(all_elements[i][ety_type_pos])
        
        print(f'{row_pos}, {col_pos}')
        data[row_pos][col_pos] += 1
    
    data.insert(0, columns)
    data.append(rows_names)
    return data
    
    
def prepare_ety_by_year_data(all_elements, headers, cs):
    remove_special_chars_year(all_elements, headers)
    fill_no_etymology(all_elements, headers)
    unique_ety_types = get_all_unique_etymology_types(all_elements, headers)
    data = prepare_year_type_data(all_elements, headers)
    save_as_csv(cs['root'], data, "ety_type_by_year", headers)

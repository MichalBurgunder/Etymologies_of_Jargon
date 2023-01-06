
import numpy as np    # to create dummy data
# from analysis_by_2nd_ety_type import get_all_unique_etymology_types
from config import find_field_position
from utils import number_only, fill_no_etymology
from file_management import save_as_csv


def count_field_types_by_scrape(data, pos, scr_ident):
    all_types = {}
    for i in range(0,len(data)):
        if data[i][pos] not in all_types:
            all_types[data[i][pos]] = 1
        else: 
            all_types[data[i][pos]] += 1
    
    return all_types

def prepare_year_type_data(all_elements, headers, scr_ident="CP"):
    print("starting 2nd ety. type analysis...")
    fill_no_etymology(all_elements, headers, fill="Unknown", field="2nd Ety. type")
    ety_type_pos = find_field_position(headers, "2nd Ety. type")
    hash_table = count_field_types_by_scrape(all_elements, ety_type_pos, scr_ident) # sets the years, so that one can query it

    x = []
    y = []
    for key, value in hash_table.items():
        x.append(key)
        y.append(value)

    data = [x, y]
    save_as_csv(data, "2nd_ety_type")
    return data
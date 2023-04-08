import os
import sys
# import time

from analysis_max_depth import populate_ety_depths, prepare_depth_data
from preparatory import get_headers_hashmap, get_element_hashmap, prepare_data, add_virtual_columns
from file_management import save_as_csv
from config import prepare_globals, fill_clean_names, root, paths, ety_depth
from utils import get_run_options
from analysis_by_year import prepare_ety_by_year_data
from analysis_number_morphemes import number_of_morphemes
from analysis_jargon_length import prepare_jargon_length
from analysis_by_2nd_ety_type import prepare_2nd_ety_type_data
from analysis_cultural_heritage import prepare_cultural_heritage_data

os.system('clear')

# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3] !!OBS!!
# lines, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

def __main__():
    # be = time.time()
    options = get_run_options(sys.argv)

    # takes from temp_debug.csv, if exists
    dataa = prepare_data(root, paths, options)
    
    # the new columns are specified by the second input
    new_headers = add_virtual_columns(dataa, [ety_depth], ["-1"])
    
    cs = prepare_globals(dataa)
    # fill_clean_names(dataa, cs)

    headers, header_hashmap = dataa[1], dataa[2]

    element_hash_map = get_element_hashmap(dataa[0], headers, cs)
    
    ready_dataa = [dataa[0], element_hash_map, headers, header_hashmap]

    populate_ety_depths(ready_dataa, cs, options)

    print("No new additives. Proceeding to analysis...")
    # -----------------------------------
    
    # prepare_ety_by_year_data(dataa[0], headers, "PL", 1)
    # prepare_ety_by_year_data(dataa[0], headers, "PL", 2)
    # prepare_jargon_length(dataa[0], headers)
    # prepare_ety_by_year_data(dataa[0], headers, "PL", 2)
    
    # prepare_2nd_ety_type_data(dataa[0], headers) # ?

    # print("done")
    # exit()
    # -----------------------------------
    # ACTUAL ANALYSIS
    # -----------------------------------
    # writes data to final_ety_depths.csv

    # depths per entry
    prepare_depth_data(dataa[0], cs)
    
    # ety types by year
    prepare_ety_by_year_data(dataa[0], headers, "PL", 1)
    prepare_ety_by_year_data(dataa[0], headers, "PL", 2)
    
    # prepare_2nd_ety_type_data(dataa[0], headers) # ? Not sure if this is useful...
    
    # basic jargon length
    prepare_jargon_length(dataa[0], headers)
    prepare_jargon_length(dataa[0], headers, "PL")
    prepare_jargon_length(dataa[0], headers, "CP")
    prepare_jargon_length(dataa[0], headers, "RG")
    prepare_jargon_length(dataa[0], headers, "PM")
    
    # number of morphemes, whole set, only specific sets
    number_of_morphemes(dataa[0], headers)
    number_of_morphemes(dataa[0], headers, "PL")
    number_of_morphemes(dataa[0], headers, "RB")
    number_of_morphemes(dataa[0], headers, "CP")
    number_of_morphemes(dataa[0], headers, "PM")
    
    
    # 2nd ety type frequency
    prepare_2nd_ety_type_data(dataa[0], headers, "PL")
    prepare_2nd_ety_type_data(dataa[0], headers, "CP")
    prepare_2nd_ety_type_data(dataa[0], headers, "RG")
    prepare_2nd_ety_type_data(dataa[0], headers, "PM")
    
    prepare_cultural_heritage_data(dataa[0], headers)
    print("All done!")
    # en = time.time()
    # print(en - be)

__main__()
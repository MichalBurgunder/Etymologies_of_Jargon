import os
import sys
# import time

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis_max_depth import populate_ety_depths, prepare_depth_data
from preparatory import get_headers_hashmap, get_element_hashmap, prepare_data, add_virtual_columns
from file_management import save_as_csv
from config import prepare_globals, fill_clean_names, root, paths, ety_depth
from utils import get_run_options, find_field_position
from analysis_by_decade import prepare_ety_by_decade_data
from analysis_number_morphemes import number_of_morphemes
from analysis_jargon_length import prepare_jargon_length
from analysis_by_2nd_ety_type import prepare_2nd_ety_type_data
from analysis_cultural_heritage import prepare_cultural_heritage_frequency_total, prepare_cultural_heritage_frequency_by_data_set
from analysis_ety_types_by_set import prepare_ety_type_counts
from analysis_influence import prepare_pagerank_data, io_algo_wrapper, reinsert_edges
from search_data import possible_search
os.system('clear')

# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3] !!OBS!!
# lines, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

def __main__():
    """
    Assuming that all necessary data is present in 'thesis_data/raw_data', 
    performs all of the analyses, and creates .csv files with their results.
    Note, that this function does NOT visualize the data
    
    All executed functions below 'ACTUAL ANALYSIS' are the data sets that
    will be created. Everything above it, are preparatory functions that
    concatenate all data from various sources, validate, clean and preprocess
    it.
    """
    # be = time.time()
    options = get_run_options(sys.argv)

    # takes from temp_debug.csv, if exists
    dataa = prepare_data(root, paths, options)

    # the new columns are specified by the second input
    new_headers = add_virtual_columns(dataa, [ety_depth], ["-1"])
    
    cs = prepare_globals(dataa)
    # fill_clean_names(dataa, cs)

    headers, header_hashmap = dataa[1], dataa[2]

    # in case we are doing an ad hoc search of the data for some string
    possible_search(dataa[0], headers)    
    
    element_hash_map = get_element_hashmap(dataa[0], headers, cs)
    
    ready_dataa = [dataa[0], element_hash_map, headers, header_hashmap]

    populate_ety_depths(ready_dataa, cs, options)

    print("No new additives. Proceeding to analysis...")
    # -----------------------------------
    
    # hs = {"GNU": 0, "PL": 0, "CP": 0, "RG": 0, "PM": 0, "ADD": 0}
    # for i in range(0, len(dataa[0])):
    #     krhjgbiejrngvak = find_field_position(headers, "Scrape Identifier")
    #     hs[dataa[0][i][krhjgbiejrngvak]] += 1
    # print(hs)
    # # print(normal)
    # exit()
    
    # prepare_ety_by_decade_data(dataa[0], headers, "PL", 1)
    # prepare_ety_by_decade_data(dataa[0], headers, "PL", 2)
    # prepare_jargon_length(dataa[0], headers)
    # prepare_ety_by_decade_data(dataa[0], headers, "PL", 2)
    
    # prepare_2nd_ety_type_data(dataa[0], headers) # ?

    # print("done")
    # exit()
    
    # -----------------------------------
    # ACTUAL ANALYSIS
    # -----------------------------------
    # writes data to final_ety_depths.csv

    # depths per entry
    # prepare_depth_data(dataa[0], cs, headers)
    
    # ety types by year
    # prepare_ety_by_decade_data(dataa[0], headers, "PL", 1)
    # prepare_ety_by_decade_data(dataa[0], headers, "PL", 2)
    
    # prepare_2nd_ety_type_data(dataa[0], headers) # ? Not sure if this is useful...
    
    # basic jargon length
    # prepare_jargon_length(dataa[0], headers)
    # prepare_jargon_length(dataa[0], headers, "PL")
    # prepare_jargon_length(dataa[0], headers, "CP")
    # prepare_jargon_length(dataa[0], headers, "RG")
    # prepare_jargon_length(dataa[0], headers, "PM")
    
    # number of morphemes, whole set, only specific sets
    # number_of_morphemes(dataa[0], headers, "ALL")
    # number_of_morphemes(dataa[0], headers, "PL")
    # number_of_morphemes(dataa[0], headers, "CP")
    # number_of_morphemes(dataa[0], headers, "RG")
    # number_of_morphemes(dataa[0], headers, "PM")
    # number_of_morphemes(dataa[0], headers, "TOP")
    
    # 2nd ety type frequency
    # prepare_2nd_ety_type_data(dataa[0], headers, "PL")
    # prepare_2nd_ety_type_data(dataa[0], headers, "CP")
    # prepare_2nd_ety_type_data(dataa[0], headers, "RG")
    prepare_2nd_ety_type_data(dataa[0], headers, "PM")
    
    # prepare_cultural_heritage_frequency_total(dataa[0], headers)
    # prepare_cultural_heritage_frequency_by_data_set(dataa[0], headers, ["GNU", "ADD", "Fix"])
    # preapre data of ety types per data set
    # prepare_ety_type_counts(dataa[0], headers, ["PL", "CP", "RG", "PM"])
    
    # influence
    # [all_pg_matricies, all_identifiers, all_submatrix_hms]
    # pg_matricies_info, edges_removed = prepare_pagerank_data(dataa[0], element_hash_map["ti"], headers, cs, True)
    # pg_matricies_info = prepare_pagerank_data(dataa[0], element_hash_map["ti"], headers, cs)
    # print(edges_removed)
    # io_algo_wrapper(pg_matricies_info[0][-1], pg_matricies_info[2][-1], cs, dataa[0])
    
    print("All done!")
    
    # en = time.time()
    # print(en - be)

__main__()
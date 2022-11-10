import os
from os.path import exists

from etymology_tree_search import add_virtual_columns, populate_ety_depths, prepare_data, get_headers_hashmap, get_element_hashmap
from file_management import save_as_csv
from config import prepare_globals, fill_clean_names, root, paths, ety_depth

os.system('clear')

# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3] !!OBS!!
# lines, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

def __main__():
    
    dataa = prepare_data(root, paths)
    
    new_headers = add_virtual_columns(dataa, [ety_depth], ["-1"])

    cs = prepare_globals(dataa)
    fill_clean_names(dataa, cs)
    
    header_hashmap, headers = get_headers_hashmap(root, paths, new_headers)

    element_hash_map = get_element_hashmap(dataa[0], headers)
    
    ready_dataa = [dataa[0], element_hash_map, headers, header_hashmap]

    if not exists(f"{cs['root']}/temp_debug.csv"):  
        # print("inside")
        save_as_csv(cs['root'], ready_dataa[0], "debug", ready_dataa[2])
    else:
        print("outside")
    
    populate_ety_depths(ready_dataa, cs)
    
    print("Additives: ")
    print(cs['additives'])
    
__main__()
import os
from os.path import exists

from etymology_tree_search import add_virtual_columns, populate_ety_depths, prepare_data, get_headers_hashmap, get_element_hashmap, prepare_depth_data, save_as_txt
from file_management import save_as_csv
from config import prepare_globals, fill_clean_names, root, paths, ety_depth

os.system('clear')

# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3] !!OBS!!
# lines, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

def __main__():
    
    # takes from temp_debug.csv, if exists
    dataa = prepare_data(root, paths)

    new_headers = add_virtual_columns(dataa, [ety_depth], ["-1"])

    cs = prepare_globals(dataa)
    fill_clean_names(dataa, cs)
    
    header_hashmap, headers = get_headers_hashmap(root, paths, new_headers)

    element_hash_map = get_element_hashmap(dataa[0], headers)
    
    # print(element_hash_map["ti"]["C#"])
    # exit()
    
    ready_dataa = [dataa[0], element_hash_map, headers, header_hashmap]

    if not exists(f"{cs['root']}/temp_debug.csv"):  
        # print("inside")
        save_as_csv(cs['root'], ready_dataa[0], "debug", ready_dataa[2])
    else:
        print("outside")
    
    # print(cs['additives'])
    # exit()
    populate_ety_depths(ready_dataa, cs)
    # print(cs['additives'])
    # exit()

    
    # deduplication of list, for better use
    new_additives = list(set(cs['additives']))
    # print("All Elements: ")
    print("Additives: ")
    print(new_additives)
    # exit() cs['root'], new_additives, "new_additives"
    save_as_csv(cs['root'], new_additives, "new_additives", ["Name"], True, True)
    
    # writes data to final_ety_depths.csv
    prepare_depth_data(dataa[0], cs)
    
__main__()
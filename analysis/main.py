import os
from os.path import exists

from etymology_tree_search import add_virtual_columns, populate_ety_depths, prepare_data
from file_management import save_as_csv
from config import prepare_globals, prepare_virtual_fields, fill_clean_names, root, paths, ety_depth

os.system('clear')

# lines, element_hash_map, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

def __main__():
    
    dataa = prepare_data(root, paths)
    add_virtual_columns(dataa, [ety_depth], ["-1"])

    cs = prepare_globals(dataa)
    print("LALALA")
    prepare_virtual_fields(dataa, cs)
    print("LALALA2")
    fill_clean_names(dataa, cs)
    print("??")
    if not exists(f"{cs['root']}/temp_debug.csv"):  
        print("inside")
        save_as_csv(cs['root'], dataa[0], "debug", dataa[2])
    print("end ??") 
    new_additives = populate_ety_depths(dataa, cs)
    
__main__()
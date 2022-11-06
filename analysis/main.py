import os
from os.path import exists

from etymology_tree_search import add_virtual_columns, populate_ety_depths, prepare_data, save_as_csv
from file_management import save_as_csv


os.system('clear')

root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data'
paths = [
            'programming_languages.csv', # programming languages
            'additives.csv'
        ]

additives = [] # here will be all the new name additives that have not been added just yet

jargon_entries = ["X1st Jargon", "X2nd Jargon", "X3rd Jargon", "X4th Jargon"] # the fields which will create our tree

ety_depth = "Etymology Depth"
clean_name = "Cleaned Name"

virtual_fields = ["ety.depth"]
vf_default_values = ['-1']


# lines, element_hash_map, headers, header_hms = dataa[0], dataa[2], dataa[3], dataa[3]


def __main__():
    dataa = prepare_data(root, paths)

    add_virtual_columns(dataa, [ety_depth], ["-1"])
    if not exists(f"{root}/temp_debug.txt"):  
        save_as_csv(root, dataa[0], "debug", dataa[2])
        
    additives = populate_ety_depths()
__main__()
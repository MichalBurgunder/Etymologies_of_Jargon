from etymology_tree_search import add_virtual_columns, populate_ety_depths, prepare_data


root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data'
paths = [
            'programming_languages.csv', # programming languages
            'additives.csv'
        ]

dataa = prepare_data(root, paths)

additives = [] # here will be all the new name additives that have not been added just yet

jargon_entries = ["X1st Jargon", "X2nd Jargon", "X3rd Jargon", "X4th Jargon"] # the fields which will create our tree

ety_depth = "Etymology Depth"
clean_name = "Cleaned Name"


dataa = prepare_data(paths)

lines, element_hash_map, headers, header_hms = dataa[0], dataa[2], dataa[3], dataa[3]


def __main__():
    print("here")
    exit()
    add_virtual_columns(dataa, ety_depth, "-1")


    additives = populate_ety_depths()

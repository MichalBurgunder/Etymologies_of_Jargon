
import numpy as np
from utils import copy_array
from file_management import save_as_txt, save_as_csv
from config import element_limit
global recur
recur = 0
recur_limit = 20
# The function that computes the max depth of an entry
def get_max_depth(data, entry, element_hashmap, header_hms, cs, previous_jargons, options={}):
    global recur

    # print('get_max_depth with entry ' + str(data[entry][cs['clean_name_pos']]) + " with depth " + str(len(previous_jargons)))
    if recur == recur_limit:
        print(f"recursion limit reached ({recur_limit})at data_entry {data[entry][cs['clean_name_pos']]}. exiting...")
        exit()
    word = data[entry][cs['clean_name_pos']]


    previous_jargons.append(word)
    
    entry = element_hashmap["ti"][word]
    
    max_depths = [-1]

    if data[entry][header_hms['ti'][cs['ety_depth']]] != "-1": # if the entry has already been computed
        if options['v']:
            print("already computed. Skipping....")
        return data[entry][header_hms['ti'][cs['ety_depth']]]
     
    # for every jargon entry   
    for j_pos in cs['jargon_entry_positions']:

        # if there is no jargon entry
        if data[entry][j_pos] == "": 
            continue
        
        # if the entry is recursive
        if data[entry][j_pos] in previous_jargons: 
            for i in range(len(previous_jargons), 0, -1):
                if previous_jargons[i-1] == word:
                    return len(previous_jargons)-i
        
        # if not existing, add to additives
        if data[entry][j_pos] not in element_hashmap['ti']:
            if options['v']:
                print(f"Adding new word to additives: {data[entry][j_pos]}")
            cs['additives'].append(data[entry][j_pos])
            continue
        
        # existing. We find it, and populate it like this entry
        row_pos = element_hashmap['ti'][data[entry][j_pos]]
        recur += 1
        prev_jarg = copy_array(previous_jargons)
        max_depth = get_max_depth(data, row_pos, element_hashmap, header_hms, cs, prev_jarg, options)
        recur -= 1
        max_depths.append(max_depth)


    return np.max(max_depths) + 1


# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

# # computes the etymology depth of any given entry
def populate_ety_depths(dataa, cs, options={}):
    print('starting ety. depth analysis')
    for i in range(1, len(dataa[0])):
        if options['v']:
            print(f"now computing {dataa[0][i][cs['clean_name_pos']]}")
        max_depth = get_max_depth(dataa[0], i, dataa[1], dataa[3], cs, [], options)
        dataa[0][i][cs['ety_depth_pos']] = max_depth
        
        if i == element_limit:
            print(f"done first {element_limit}")
            print(f"additives: {cs['additives']}")
            save_as_txt(cs['root'], cs['additives'], 'additives')
            exit()
    return 

def prepare_depth_data(data, cs):
    final_data = []
    for i in range(0, len(data)):
        final_data.append([data[i][cs["clean_name_pos"]], data[i][cs['ety_depth_pos']]])
    
    save_as_csv(final_data, "ety_depths")


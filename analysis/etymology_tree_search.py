import csv
import numpy as np
import os
from os.path import exists
from utils import concatenate, copy_array
from file_management import write_into_one_csv, save_as_txt, save_as_csv
from config import find_field_position, get_run_options, clean_name, debug, raw_data_root
import sys

global element_hash_map
global run_options
    
limit = 1500 if not debug else 10
    
def header_hashmaps(headers, other_headers):
    head_i_hm = {}
    i_head_hm = {}
    
    for i in range(0, len(headers)):
        i_head_hm[i] = headers[i]
        head_i_hm[headers[i]] = i
    
    inc = len(headers)
    for i in range(0, len(other_headers)):
        i_head_hm[i] = other_headers[i]
        head_i_hm[other_headers[i]] = inc + i
        inc += 1
    return {"it": i_head_hm, "ti": head_i_hm}


def get_headers(path):
    with open(path) as file:
            return next(file)

def merge_csv_headers(root, paths):
    headerss = []
    path = write_into_one_csv(root, paths, "headers", True)
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0, len(paths)):  
        headerss.append(next(file))
    
    os.remove(path)
    return headerss

def merge_csv_data(root, paths):
    lines = []
    path = write_into_one_csv(root, paths, "data")
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0,len(paths)):  
        lines.append(next(file))
    
    os.remove(path)
    return

def get_headers_hashmap(root, paths, virtual_fields=[]):
    headerss = merge_csv_headers(root, paths)

    # we verify: length
    num_headers = len(headerss[0])
    for i in range(1,len(headerss)):
        if False in [len(headerss[i]) == num_headers for headers in headerss]:
            raise Exception("Length of the headers are not the same:\n" + str(headerss))

    # we verify: each entry
    for i in range(0, num_headers):
        for j in range(1, len(headerss)):
            if headerss[0][i] != headerss[j][i]:
                raise "Entries in headers are not the same"

    return header_hashmaps(headerss[0], virtual_fields), concatenate(headerss[0], virtual_fields)

def get_element_hashmap(data, headers):    
    clean_name_pos = find_field_position(headers, clean_name)  
    element_hashmap = {"ti": {}, "it": {}}
    
    for i in range(0, len(data)):
        element_hashmap["ti"][data[i][clean_name_pos]] = i
        element_hashmap["it"][i] = data[i][clean_name_pos]
    return element_hashmap
    
    
def prepare_data(root, paths, options={}):
    global clean_name_pos
    global limit
    
    errors = False
    path = None
    if not exists(f"{root}/temp_debug.csv") and debug == False:  
        path = write_into_one_csv(root, paths, "data")
    else:
        path = f"{root}/temp_debug.csv"
    
    file = csv.reader(open(path, mode ='r'))
    header_hashmap, headers = get_headers_hashmap(root, paths)
    
    sem_num = find_field_position(headers, 'Semantic number')
    clean_name_pos = find_field_position(headers, 'Cleaned Name')
    
    all_elements = []
    name_hm = {}
    
    i = 0
    for line in file:
        
        if line[sem_num] != '2':# and line[sem_num] != '3': # not adding line semantic numbers 2 (error in scraping) or 3 (proto additive)
            if line[clean_name_pos] in name_hm:
                print(f"Duplicate entry found for {line[clean_name_pos]}. Skipping...")
                errors = True
            else:
                all_elements.append(line)
                name_hm[line[clean_name_pos]] = True
        else:
            continue
        
        if i == limit:
            if run_options['v']:
                print("exiting here")
            return all_elements, headers, header_hashmap
        i += 1
    
    if errors:
        print("Fix the errors, and run the file again.")
        exit()
    return all_elements, headers, header_hashmap

def add_virtual_columns(dataa, names, default_values):
    # all_elements, element_hash_map, headers, header_hashmap = dataa[0], dataa[1], dataa[2], dataa[3]
    
    for i in range(0,len(names)):
        dataa[1].append(names[i]) # add to headers
        dataa[2]["ti"][names[i]] = len(dataa[1])-1 # add to headers hashmap
        dataa[2]["it"][len(dataa[1])] = names[i] # add to headers hashmap
    
        for j in range(0, len(dataa[0])): # add the default value to each entry
            dataa[0][j].append(default_values[i])

    return names
global recur
recur = 0 
# The function that computes the max depth of an entry
def get_max_depth(data, entry, element_hashmap, header_hms, cs, previous_jargons, options={}):
    global recur

    # print('get_max_depth with entry ' + str(data[entry][cs['clean_name_pos']]) + " with depth " + str(len(previous_jargons)))
    if recur == 6:
        print(f"recursion limit reached at data_entry {data[entry][cs['clean_name_pos']]}. exiting...")
        exit()
    word = data[entry][cs['clean_name_pos']]

    previous_jargons.append(word)
    
    entry = element_hashmap["ti"][word]
    
    max_depths = [0]

    if data[entry][header_hms['ti'][cs['ety_depth']]] != "-1": # if the entry has already been computed
        if options['v']:
            print("already computed. Skipping....")
        return data[entry][header_hms['ti'][cs['ety_depth']]]
        
    for j_pos in cs['jargon_entry_positions']:

        if data[entry][j_pos] == "": # if there is no jargon entry
            continue
        
        if data[entry][j_pos] in previous_jargons: # if the entry is recursive
            for i in range(len(previous_jargons), 0, -1):
                if previous_jargons[i-1] == word:
                    return len(previous_jargons)-i
        
        # jargon must be there, and uncomputed. Check if not existing, then add
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


    return np.max(max_depths)


# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

# # computes the etymology depth of any given entry
def populate_ety_depths(dataa, cs, options={}):
    global limit

    
    for i in range(1, len(dataa[0])):
        if options['v']:
            print(f"now computing {dataa[0][i][cs['clean_name_pos']]}")
        max_depth = get_max_depth(dataa[0], i, dataa[1], dataa[3], cs, [], options)
        dataa[0][i][cs['ety_depth_pos']] = max_depth
        
        if i == limit:
            print(f"done first {limit}")
            print(f"additives: {cs['additives']}")
            save_as_txt(cs['root'], cs['additives'], 'additives')
            exit()
    return 

def merge_csv_headers(root, paths):
    headerss = []

    path = write_into_one_csv(root, paths, "headers", True)
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0, len(paths)):  
        headerss.append(next(file))
    
    os.remove(path)
    return headerss

# notes:
# Volume of a node can refer to the authority of the node (refers to the name obfuscation, e.g. how likely one is able to guess the etymology of a word)
# Hub node: See HITS


def prepare_depth_data(data, cs):
    final_data = []
    for i in range(0, len(data)):
        final_data.append([data[i][cs["clean_name_pos"]], data[i][cs['ety_depth_pos']]])
    
    save_as_csv(cs['root'], final_data, "final_ety_depths", final_data[0])

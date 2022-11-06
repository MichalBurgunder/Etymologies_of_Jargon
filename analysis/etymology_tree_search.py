import csv
from re import I
import pandas as pd
from os import system
import time
import numpy as np
import os
from os.path import exists

from file_management import write_into_one_csv
from config import find_field_position, prepare_virtual_fields, clean_name

global element_hash_map

def header_hashmaps(headers):
    head_i_hm = {}
    i_head_hm = {}
    
    for i in range(0,len(headers)):
        i_head_hm[i] = headers[i]
        head_i_hm[headers[i]] = i
    return {"it": i_head_hm, "ti": head_i_hm}


def get_headers(path):
    with open(path) as file:
            return next(file)

def merge_csv_headers(root, paths):
    headerss = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    # with open(f"{root}/temp.txt", "wt") as fw:
    #     writer = csv.writer(fw)
    #     for path in paths:
    #         with open(f"{root}/{path}") as file:
    #             info = csv.reader(file, delimiter=',')
                
    #             for row in info:
    #                 writer.writerow(row)
    # #                 break
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

def get_headers_hashmap(root, paths):
    headerss = merge_csv_headers(root, paths)

    # we verify: length
    num_headers = len(headerss[0])
    if False in [len(headers) == num_headers for headers in headerss]:
        raise "Length of the headers are not the same:\n" + str(headerss)
    print()
    # we verify: each entry
    for i in range(0, num_headers):
        for j in range(1, len(headerss)):
            if headerss[0][i] != headerss[j][i]:
                print(headerss[0][i])
                print(headerss[j][i])
                raise "Entries in headers are not the same"

    return header_hashmaps(headerss[0]), headerss[0]
    
def prepare_data(root, paths):
    global clean_name_pos
     
    all_elements = []
    element_hashmap = {"ti": {}, "it": {}}
    
    path = None
    if not exists(f"{root}/temp_debug.csv"):  
        path = write_into_one_csv(root, paths, "data")
    else:
        path = f"{root}/temp_debug.txt"
    
    file = csv.reader(open(path, mode ='r'))
    

    
    header_hashmap, headers = get_headers_hashmap(root, paths)
    sem_num = find_field_position(headers, 'Semantic number')

    for line in file:
        if line[sem_num] != '2': # not adding line semantic numbers 2 (error in scraping)
            all_elements.append(line) 

    clean_name_pos = find_field_position(headers, clean_name)
    
    for i in range(0, len(all_elements)):
        element_hashmap["ti"][all_elements[i][clean_name_pos]] = i
        element_hashmap["it"][i] = all_elements[i][clean_name_pos]

    return all_elements, element_hashmap, headers, header_hashmap

def add_virtual_columns(dataa, names, default_values):
    # all_elements, element_hash_map, headers, header_hashmap = dataa[0], dataa[1], dataa[2], dataa[3]
    
    for i in range(0,len(names)):
        dataa[2].append(names[i]) # add to headers
        dataa[3]["ti"][names[i]] = len(dataa[2])-1 # add to headers hashmap
        dataa[3]["it"][len(dataa[2])] = names[i] # add to headers hashmap
    
        for j in range(0, len(dataa[0])): # add the default value to each entry
            # print(len(dataa[0][j]))
            dataa[0][j].append(default_values[i])
            # print(len(dataa[0][j]))
            # exit()
    # 
    # exit()
global recur
recur = 0 
# The function that computes the max depth of an entry
def populate_depth(data, entry, element_hashmap, header_hms, cs, previous_jargons=[]):
    global recur
    print(f'populate_depth with entry {data[entry]}')
    if recur == 6:
        exit()
    word = data[entry][cs['clean_name_pos']]

    previous_jargons.append(word)
    if word not in element_hashmap["ti"]:
        if word not in cs['additives']:
            cs['additives'].append(word)
        return -1
    
    entry = element_hashmap["ti"][word]
    
    max_depths = [0]

    # print(cs)
    # exit()
    for j_pos in cs['jargon_entry_positions']:
        print(data[entry][header_hms['ti'][cs['ety_depth']]])
        if data[entry][header_hms['ti'][cs['ety_depth']]] != "-1": # if the entry has already been computed
            return data[entry][header_hms['ti'][cs['ety_depth']]]
        
        print(data[entry][j_pos])
        if data[entry][j_pos] == "": # if there is no jargon entry
            continue
        
        if data[entry][j_pos] in previous_jargons: # if the entry is recursive
            for i in range(len(previous_jargons), 0, -1):
                if previous_jargons[i] == word:
                    return len(previous_jargons)-i
        
        # jargon must be there, and uncomputed
        row_pos = element_hashmap['ti'][data[entry][j_pos]]
       
        recur += 1
        max_depth = populate_depth(data, row_pos, element_hashmap, header_hms, cs, previous_jargons)
        max_depths.append(max_depth)

    return np.max(max_depths)


# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

# # computes the etymology depth of any given entry
def populate_ety_depths(dataa, cs):
    for i in range(0, len(dataa[0])):
        populate_depth(dataa[0], i, dataa[1], dataa[3], cs)
        if i == 3:
            print("done first 3")
            exit()


    
# def read_from_csv(root, descriptor):
# def get_data(root, title):
#     if exists(f"{root}/{title}"):
#         res = []
#         with open(f"{root}/temp_{descriptor}", "wt") as fw:
#             for row in fw:
#                 res.append(row)
#     else:
#         data = prepare_data(root, )
#         save_as_csv(root, data, title)
#         return data
    

def merge_csv_headers(root, paths):
    headerss = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    # with open(f"{root}/temp.txt", "wt") as fw:
    #     writer = csv.writer(fw)
    #     for path in paths:
    #         with open(f"{root}/{path}") as file:
    #             info = csv.reader(file, delimiter=',')
                
    #             for row in info:
    #                 writer.writerow(row)
    # #                 break
    path = write_into_one_csv(root, paths, "headers", True)
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0, len(paths)):  
        headerss.append(next(file))
    
    os.remove(path)
    return headerss
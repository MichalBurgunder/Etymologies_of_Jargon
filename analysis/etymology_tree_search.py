import csv
from re import I
import pandas as pd
from os import system
import time
import numpy as np
import os
system('clear')

global ety_depth
global clean_name
global element_hash_map

def header_hashmaps(headers):
    head_i_hm = {}
    i_head_hm = {}
    
    for i in range(0,len(headers)):
        i_head_hm[i] = headers[i]
        head_i_hm[headers[i]] = i
    return {"it": i_head_hm, "ti": head_i_hm}
      
def find_clean_name_position(headers):
    for i in range(0,len(headers)):
        if headers[i] == "Cleaned Name":
            return i
    raise "Cannot find 'Cleaned Name' column"


def get_headers(path):
    with open(path) as file:

            return next(file)

def merge_csv_headers(root, paths):
    headerss = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/temp.txt", "wt") as fw:
        writer = csv.writer(fw)
        for path in paths:
            with open(f"{root}/{path}") as file:
                info = csv.reader(file, delimiter=',')
                
                for row in info:
                    writer.writerow(row)
                    break
    
    file = csv.reader(open(f"{root}/temp.txt", mode ='r'))
    for i in range(0,len(paths)):  
        headerss.append(next(file))
    
    os.remove(f"{root}/temp.txt")
    return headerss

def merge_csv_data(root, paths):
    lines = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/temp.txt", "wt") as fw:
        writer = csv.writer(fw)
        for path in paths:
            with open(f"{root}/{path}", ) as file:
                info = csv.reader(file, delimiter=',')
                next(info) # in an attempt to skip the header
                for row in info:
                    writer.writerow(row)
    
    file = csv.reader(open(f"{root}/temp.txt", mode ='r'))
    for i in range(0,len(paths)):  
        lines.append(next(file))
    
    os.remove(f"{root}/temp.txt")
    return headerss




def get_headers_hashmap(root, paths):
    headerss = merge_csv_headers(root, paths)

    # we verify: length
    num_headers = len(headerss[0])
    if False in [len(headers) == num_headers for headers in headerss]:
        raise "Length of the headers are not the same:\n" + str(headerss)
    
    # we verify: each entry
    for i in range(0, num_headers):
        for j in range(1, len(headerss)):
            if headerss[0][i] != headerss[j][i]:
                raise "Entries in headers are not the same"

    return header_hashmaps(headerss[0]), headerss[0]

def write_into_one_csv(root, paths):
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/temp.txt", "wt") as fw:
        writer = csv.writer(fw)
        for path in paths:
            with open(f"{root}/{path}", ) as file:
                info = csv.reader(file, delimiter=',')
                next(info) # in an attempt to skip the header
                for row in info:
                    # print("la")
                    writer.writerow(row)
    
def prepare_data(root, paths):
    all_elements = []
    element_hash_map = {}
    header_hashmap, headers = get_headers_hashmap(root, paths)
    clean_name_pos = find_clean_name_position(headers)
    
    # merge_csv_data()
    
    lines = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/temp.txt", "wt") as fw:
        writer = csv.writer(fw)
        for path in paths:
            with open(f"{root}/{path}", ) as file:
                info = csv.reader(file, delimiter=',')
                next(info) # in an attempt to skip the header
                for row in info:
                    # print("la")
                    writer.writerow(row)
    
    file = csv.reader(open(f"{root}/temp.txt", mode ='r'))
    
    for line in file:
        lines.append(line)
    
    os.remove(f"{root}/temp.txt")

    # for i in paths:
    #     print(i)
    #     file = csv.reader(open(paths[i], mode ='r'))
    #     i = 1
    #     for line in file:
    #         all_elements.append(line)
    #         element_hash_map[line[clean_name_pos]] = i
    #         i += 1
    exit()
    return all_elements, element_hash_map, headers, header_hashmap

def add_virtual_columns(dataa, names, default_values):
    # all_elements, element_hash_map, headers, header_hashmap = dataa[0], dataa[1], dataa[2], dataa[3]
    for i in names:
    
        dataa[2].append(names[i]) # add to headers
        dataa[3]["ti"][names[i]] = len(dataa[2])-1 # add to headers hashmap
        dataa[3]["it"][len(dataa[2])] = names[i] # add to headers hashmap
    
        for j in range(0,len(dataa[0])): # add the default value to each entry
            dataa[0][j].append(default_values[j])
 

# programming languages
# paths = [
#             '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/programming_languages.csv',
#             '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/additives.csv'
# #         ]

# dataa = prepare_data(paths)

# lines, element_hash_map, headers, header_hms = dataa[0], dataa[2], dataa[3], dataa[3]

# additives = [] # here will be all the new name additives that have not been added just yet

# jargon_entries = ["X1st Jargon", "X2nd Jargon", "X3rd Jargon", "X4th Jargon"] # the fields which will create our tree

# ety_depth = "Etymology Depth"
# clean_name = "Cleaned Name"

# add_virtual_columns(dataa, ety_depth, "-1")
        

# The function that computes the max depth of an entry
def populate_depth(word, previous_jargons=[]):
    previous_jargons.append(word)
    if word not in element_hash_map["ti"]:
        if word not in additives:
            additives.append(word)
        return -1
    
    entry = element_hash_map["ti"][word]
    
    max_depths = [0]
    for j in range(0, jargon_entries):
        if lines[entry][ety_depth] != "-1": # if the entry has already been computed
            return lines[entry][ety_depth]
        
        if lines[entry][j] == "": # if there is no jargon entry
            continue
        
        if lines[entry][j] in previous_jargons: # if the entry is recursive
            for i in range(len(previous_jargons), 0, -1):
                if previous_jargons[i] == word:
                    return len(previous_jargons)-i
        
        # jargon must be there, and uncomputed
        max_depth = populate_depth(lines[entry][j], previous_jargons)
        max_depths.append(max_depth)
        
    return np.max(max_depths)
    
# # computes the etymology depth of any given entry
def populate_ety_depths(dataa):
    for i in range(0, len(lines)):
        populate_depth(lines[i])

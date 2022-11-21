import csv
import os
from utils import concatenate
from file_management import write_into_one_csv
from config import find_field_position, clean_name, debug, element_limit

global element_hash_map
global run_options
    
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
            print(f"Length of the headers are not the same:\nLength of first headers: {num_headers}\nLength of your headers: {len(headerss[i])}")
            exit()

    # we verify: each entry
    errors = []
    for i in range(0, num_headers):
        for j in range(1, len(headerss)):
            if headerss[0][i] != headerss[j][i]:
                errors.append([headerss[0][i], headerss[j][i]])
                # print(f"Entries in headers are not the same\nOriginal header: {headerss[0][i]}\nYour header: {headerss[j][i]}")
                

    if 0 < len(errors):
        print("Entries in headers are not the same")
        for pair in errors:
            print(f"Original header: {pair[0]}\nYour header: {pair[1]}\n")
        exit()
        
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
    global element_limit
    
    errors = False
    path = None
    if not os.path.exists(f"{root}/temp_debug.csv") and debug == False:  
        path = write_into_one_csv(root, paths, "data")
    else:
        path = f"{root}/temp_debug.csv"
    
    file = csv.reader(open(path, mode ='r'))
    header_hashmap, headers = get_headers_hashmap(root, paths)
    
    sem_num = find_field_position(headers, 'Semantic number')
    clean_name_pos = find_field_position(headers, 'Cleaned Name')
    scrape_name_pos = find_field_position(headers, 'Scrape Name')
    
    all_elements = []
    name_hm = {}
    
    i = 0
    for line in file:
        
        # not adding line semantic numbers 2 (beginning/end scrape links), 3 (duplicate), 9 (false scrape), 10 (not included in anaylsis)
        if line[sem_num] not in ['2','3','9', '10']:
            if line[clean_name_pos] in name_hm:
                if line[clean_name_pos] == '':
                    print(f'Clean name empty (for scrape entry {line[scrape_name_pos]})')
                else:
                    print(f"Duplicate entry found for {line[clean_name_pos]}. Skipping...")
                errors = True
            else:
                all_elements.append(line)
                name_hm[line[clean_name_pos]] = True
        else:
            continue
        
        if i == element_limit:
            if run_options['v']:
                print("exiting here")
            return all_elements, headers, header_hashmap
        i += 1
    
    if errors:
        print("Fix the errors, and run the file again.")
        exit()
    if options['c']:
        print("Data Correct (correct headers, no duplicates, names present)\nReady to proceed")
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

# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

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
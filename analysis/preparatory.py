import csv
import os
import copy
from utils import concatenate
from file_management import write_into_one_csv
from config import find_field_position, clean_name, debug, element_limit, scrape_identifier, invalid_semantic_numbers

global element_hash_map
global run_options


def get_additive_second_names(data, headers, element_hashmap, duplicates):
    """
    In order to allow for additives to have multiple names (one alias) we include
    this function that maps the aliases onto the jargon in question. The function
    simple adds these terms to the primary element_hashmap, so that they are
    indistinguishable from norma elements
    """
    scr_name_pos = find_field_position(headers, "Scrape Name")
    scr_iden_pos = find_field_position(headers, "Scrape Identifier")
    clean_name_pos = find_field_position(headers, "Cleaned Name")
    
    for i in range(0, len(data)):
        if data[i][scr_iden_pos] == "ADD" and data[i][scr_name_pos] != "":
            if data[i][scr_name_pos] not in element_hashmap["ti"]:
                element_hashmap["ti"][data[i][scr_name_pos]] = i
                element_hashmap["it"][i] = data[i][scr_name_pos]
            else:
                duplicates.append([data[i][scr_name_pos], data[i][scr_iden_pos], data[element_hashmap["ti"][data[i][clean_name_pos]]][scr_iden_pos]])
     
def header_hashmaps(headers, other_headers):
    """
    Creates two hashmaps, that map the header name to a position, and a position
    to a header name
    """
    head_i_hm = {}
    i_head_hm = {}
    
    for i in range(0, len(headers)):
        i_head_hm[i] = headers[i]
        head_i_hm[headers[i]] = i
    
    inc = len(headers)
    for i in range(0, len(other_headers)):
        i_head_hm[inc + i] = other_headers[i]
        head_i_hm[other_headers[i]] = inc + i
        inc += 1
    return {"it": i_head_hm, "ti": head_i_hm}


def get_headers(path):
    """
    Fetches all of the used headers for a spefici file
    """
    with open(path) as file:
            return next(file)

def merge_csv_headers(root, paths):
    """
    Concatenates all headers of multiple .csv files into a matrix
    """
    headerss = []
    path = write_into_one_csv(root, paths, "headers", True)
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0, len(paths)):  
        headerss.append(next(file))
    
    os.remove(path)
    return headerss

def merge_csv_data(root, paths):
    """
    Concatenates all data included in .csv files into a single matrix
    """
    lines = []
    path = write_into_one_csv(root, paths, "data")
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0,len(paths)):  
        lines.append(next(file))
    
    # given that this data might want to be exported to somewhere else,
    # uncomment the line below to retain the full .csv file of all data
    os.remove(path)
    return

def get_headers_hashmap(root, paths, virtual_fields=[]):
    """
    Error handling wrapper to validate the inputted data for length 
    and whitespace-stripped value of headers.
    
    Returns [[two hashmaps], [all headers]]: 
    
    (1) Hashmap that maps the value of a header into the integer position where it is located
    (2) Hashmap that maps the position of a header in the array into the value of that position
    
    "All headers" are simply all headers used, actual and virtual
    """
    headerss = merge_csv_headers(root, paths)

    # we verify: length
    num_headers = len(headerss[0])

    for i in range(1,len(headerss)):
        if False in [len(headerss[i]) == num_headers for headers in headerss]:
            print(f"""Length of the headers are not the same:\n
                  Length of first headers: {num_headers}\n
                  Length of headers in pos. {i}: {len(headerss[i])}""")           
            min_num = min(len(headerss[0]), len(headerss[1]))
  
            for j in range(0, min_num):
                print(f'{headerss[0][j]} | {headerss[i][j]}')
            exit()
            
    
    # we strip each header of whitespace, to get appropriate headers
    for i in range(0, num_headers):
        for j in range(1, len(headerss)):
            headerss[j][i] =  headerss[j][i].strip()

    # we verify: each entry
    errors = []
    for i in range(0, num_headers):
        for j in range(1, len(headerss)):
            if headerss[0][i] != headerss[j][i]:
                errors.append([headerss[0][i], headerss[j][i]])
                

    # we check for errors. If none, we create the hashmaps 
    if 0 < len(errors):
        print("Entries in headers are not the same")
        for pair in errors:
            print(f"Original header: {pair[0]}\nYour header: {pair[1]}\n")
        exit()
    
    return header_hashmaps(headerss[0], virtual_fields), concatenate(headerss[0], virtual_fields)

def get_element_hashmap(data, headers, cs):
    """
    Validates uniqueness of the "Cleaned Name" value of all data
    points and creates a nested hashmap (from them) of two fields: 
    
    (1) "ti", that maps the "text" "Cleaned Name" value of a data point
    to the "integer" position in the matrix
    (2) "it", that maps the "integer" position in the matrix to the "text"
    "Cleaned Name" value of a data point
    """ 
    clean_name_pos = find_field_position(headers, clean_name)  
    scrape_identifier_pos = find_field_position(headers, scrape_identifier)  

    element_hashmap = {"ti": {}, "it": {}}
    
    duplicates = []
    
    for i in range(0, len(data)):
        if data[i][clean_name_pos] in element_hashmap["ti"]:
            duplicates.append([data[i][clean_name_pos], data[i][scrape_identifier_pos]])
        else:
            element_hashmap["ti"][data[i][clean_name_pos]] = i
            element_hashmap["it"][i] = data[i][clean_name_pos]
    
    # we include additive aliases, in order to manage mistakenly adding two of the same additive jargons
    get_additive_second_names(data, headers, element_hashmap, duplicates) 
    
    if len(duplicates) > 0:
        print("Duplicate entries found upon lowercasing them:\n")
        print(f"Clean Name | Scrape Identifier Duplicate | Scrape Identifier Original")
        for i in range(0, len(duplicates)):
            print(f"{duplicates[i][0]} | {duplicates[i][1]} | {duplicates[i][2]}")
        print("Remove duplicates from lists to proceed to analysis")
        exit()

    return element_hashmap
    
def verify_no_duplicate_jargons(data, headers):
    """
    Verifies that jargons of a data point are not documented.
    If they are, it prints out the name of the point in question, and its 
    """
    clean_name_pos = find_field_position(headers, 'Cleaned Name')
    scrap_name_pos = find_field_position(headers, 'Scrape Identifier')
    jargon_poss = [
            find_field_position(headers, '1st Jargon'),
            find_field_position(headers, '2nd Jargon'),
            find_field_position(headers, '3rd Jargon'),
            find_field_position(headers, '4th Jargon')
        ]
        
    strings = []
    for i in range(0, len(data)):
        jargons = []
        for j_pos in jargon_poss:
            if data[i][j_pos] != '':
                jargons.append(data[i][j_pos])

        set_jargons = list(set(jargons))
        if len(jargons) != len(set_jargons):
            strings.append(data[i][clean_name_pos], data[i][scrap_name_pos])

    if len(strings):
        print("Duplicate jargons mentions found for singular data points:")
        for i in range(0, len(0, len(strings))):
            print(f"Point: {strings[0]} Scrape Identifier: {strings[1]}")
        print("Fix these issues before rerunning this program")
        exit()
    
    
def prepare_data(root, paths, options={}):
    """
    Performs all validations and key variable creation used for
    the analysis of the the data included in the "paths" variable
    
    Possible options: 
    
    v: verbose
    c: check (exits the function upon data validation)
    """
    global clean_name_pos
    global element_limit
    
    errors = False
    path = None
    
    header_hashmap, headers = get_headers_hashmap(root, paths, ["Original Clean Name"]) 
    # we check if a temp file exists. If not, we reload all data from scratch
    # if not os.path.exists(f"{root}/temp_data.csv") and debug == False:  
        # writing all data in one csv, so that we can analyze them all together
    path = write_into_one_csv(root, paths, "data")
    # else:
        # we only use this route for hard to debug errors
    # path = f"{root}/temp_data.csv"
    
    # we add a virtual field, so that we may get the actual name back afterwards
    
    sem_num = find_field_position(headers, 'Semantic number')
    clean_name_pos = find_field_position(headers, 'Cleaned Name')
    scrape_name_pos = find_field_position(headers, 'Scrape Name')
    scrape_identifier_pos = find_field_position(headers, 'Scrape Identifier')
    
    to_clean_fields = [
        clean_name_pos,
        find_field_position(headers, '1st Jargon'),
        find_field_position(headers, '2nd Jargon'),
        find_field_position(headers, '3rd Jargon'),
        find_field_position(headers, '4th Jargon')
    ]
    all_elements = []
    name_hm = {}
    
    i = 0
    
    file = csv.reader(open(path, mode ='r'))
    # names = []
    for line in file:
        clean_name_original = copy.copy(line[clean_name_pos])
        # we clean the certain fields, so as not to get differently whitespaced, or capitalized jargons
        for dirty_field_pos in to_clean_fields:
            line[dirty_field_pos] = line[dirty_field_pos].lower().strip()
        
        # in case its an additive, let us also clean the scrape name, which acts as an alias
        if line[scrape_identifier_pos] == "ADD":
             line[scrape_name_pos] = line[scrape_name_pos].lower().strip()
             
        # not adding line semantic numbers 2 (beginning/end scrape links), 3 (duplicate), 9 (false scrape), 10 (not included in analysis)
        if line[sem_num] not in invalid_semantic_numbers:
            if line[clean_name_pos] == '':
                print(f'Clean name empty (for scrape entry {line[scrape_name_pos]}, scrape identifier {line[scrape_identifier_pos]})')
                errors = True
            elif line[clean_name_pos] in name_hm:
                print(f"Duplicate entry found for {line[clean_name_pos]} (scrape identifier: {line[scrape_identifier_pos]}). Skipping...")
                errors = True
            else:
                # adding the line to the data to be processed
                all_elements.append(line)
                # we add the additional field
                all_elements[len(all_elements)-1].append(clean_name_original)
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
    
    verify_no_duplicate_jargons(all_elements, headers)

    return all_elements, headers, header_hashmap

def add_virtual_columns(dataa, names, default_values):
    """
    Adds all virtual columns to be added to the data matrix
    """
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
    """
    Returns an array of the headers of multiple .csv files
    """
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
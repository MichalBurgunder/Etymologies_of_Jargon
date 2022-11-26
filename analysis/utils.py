import re
import numpy as np

def concatenate(a1, a2):
    for e in a2:
        a1.append(e)
    return a1

def copy_array(arr):
    new = []
    for el in arr:
        new.append(el)
    return new

special_chars = ["<", ">", "~", "?", "=", "s"]

def number_only(string):
    if re.search("^[0-9]{4}-[0-9]{4}$", string):
        # a range is given. we compute the middle
        return int(np.round((int(string[0:4]) + int(string[5:9]))/2)) 
    if len(string) >= 5 and string[4] == 's':
        # also a range, but we simply take the middle 
        return int(string[0:4])+5
    final = ""
    for char in string:
        if char not in special_chars:
            final += char
            
    if final == '':
        return -1
    return int(final)

def fill_no_etymology(all_elements, headers):
    ety_pos = find_field_position(headers, "Ety. type")
    for i in range(0,len(all_elements)):
        if all_elements[i][ety_pos] == "":
            all_elements[i][ety_pos] = "Missing"
    
def find_field_position(headers, field):
    for i in range(0, len(headers)):
        if headers[i] == field:
            return i
    print(f'Cannot find "{field}" column. Exiting...')
    exit()

def get_run_options(args):
    options = {
        "v": False,
        "c": False
    }
    if 1 < len(args):
        clean_args = args[1].replace('-', '', 1)

        if clean_args == args[1]:
            print("Unknown additional argument. Exiting...")
            exit()
        
        if "v" in clean_args:
            options['v'] = True
        if "c" in clean_args:
            options['c'] = True
        
    return options
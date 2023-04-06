import re
import numpy as np

def concatenate(a1, a2):
    """
    Copies all of the elements of array a2, into a1
    """
    for e in a2:
        a1.append(e)
    return a1

def copy_array(arr):
    """
    Copies an array, without worry about passing a reference
    """
    new = []
    for el in arr:
        new.append(el)
    return new

special_chars = ["<", ">", "~", "?", "=", "s"]

def number_only(string):
    """
    Given that the years are documented in ranges, this function removes
    any special characters that might be included in the data source,
    and takes a best guess on what year might be meant
    """
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

def fill_no_etymology(all_elements, headers, scrape_ident='', fill="Missing", field="Ety. type"):
    """
    For all those data that do not have the "Etymology" field filled out, we
    insert a custom text into this field.
    """
    ety_pos = find_field_position(headers, field)
    scrape_ident_pos = find_field_position(headers, 'Scrape Identifier')
    for i in range(0,len(all_elements)):
        if all_elements[i][ety_pos] == "" and (all_elements[i][scrape_ident_pos] == scrape_ident or scrape_ident == ''):
            all_elements[i][ety_pos] = fill
            
    return
    
def find_field_position(headers, field):
    """
    Searches through the available headers and returns the array
    position at which a given string can be found.
    """
    for i in range(0, len(headers)):
        if headers[i] == field:
            return i
    print(f'Cannot find "{field}" column. Exiting...')
    exit()

def get_run_options(args):
    """
    Takes all of the manually typed in options in the CLI, and formally
    documents them for further use in the program.
    """
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

def print_errors(errors):
    """
    Simply prints out the errors that are fed into it.
    """
    res = ""
    for err in errors:
        res += err + "\n"
    print(res)
    

def clean_scrape_name(name):
    return 'ALL' if name == '' else name
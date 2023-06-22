from utils import find_field_position
from config import jargon_entries

unallowed = ["gnu", "pip"]

def create_etymology(data, hm, name, headers, iteration_num=1, simple=True):
    """
    basic etymology creator. Hi audience!
    """
    name_pos = hm[name]
    explanation = find_field_position(headers, "Explanation")
    
    if not simple:
        print("-- "*iteration_num + data[name_pos][explanation])
    for j in jargon_entries:
        j_pos = find_field_position(headers, j)
        if data[name_pos][j_pos] != "" and data[name_pos][j_pos] not in unallowed:
            print("-- "*iteration_num + data[name_pos][j_pos])

            
            create_etymology(data, hm, data[name_pos][j_pos], headers, iteration_num+1)
    # if not intermediary:
    
    return 
    
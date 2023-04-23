from utils import find_field_position
import sys

def possible_search(data, headers):
    """
    Given that data sets are split across multiple sources, this function
    allows one to search for all data inputted into the system, filtering
    for a field and a value 
    """
    if len(sys.argv) == 4 and sys.argv[1] == "-s":
        field = sys.argv[2]
        value = sys.argv[3]
            
        the_pos = find_field_position(headers, field)
        
        for i in range(0, len(data)):
            if data[i][the_pos] == value:
                print(data[i])
        exit()
    return

from utils import  find_field_position
from file_management import save_as_csv

def prepare_jargon_length(data, headers):
    """
    Collects all data necessary to anaylze and graph the length of jargons. 
    It saves the data into a name_length.csv
    """
    print("starting jargon length analysis...")
    clean_name_pos = find_field_position(headers, 'Cleaned Name')

    the_max = max([len(line[clean_name_pos]) for line in data])
    final_data = [0] * (the_max+1)

    for i in range(0, len(data)):
        final_data[len(data[i][clean_name_pos])] += 1
    
    save_as_csv([[i for i in range(0, the_max)], final_data], 'name_length')

from utils import  find_field_position
from file_management import save_as_csv

def prepare_jargon_length(data, headers):
    print("starting jargon length analysis...")
    clean_name_pos = find_field_position(headers, 'Cleaned Name')
    print(clean_name_pos)
    the_max = max([len(line[clean_name_pos]) for line in data])
    final_data = [0] * (the_max+1)
    # print(the_max)
    for i in range(0, len(data)):
        # print(data[i])
        # print(len(data[i][clean_name_pos]))
        final_data[len(data[i][clean_name_pos])] += 1
    
    save_as_csv([[i for i in range(0, the_max)], final_data], 'name_length')
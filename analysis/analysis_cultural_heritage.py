

from config import find_field_position, illegal_cultural_heritage_subclasses
from file_management import save_as_csv

def prepare_cultural_heritage_data(data, headers):
    '''
    Counts the frequency of different Cultural Heritage enumerations within a given dataset 
    '''
    hash_table_ch = {}
    ch_pos = find_field_position(headers, "Cultural Heritage (CH)")
    ch_subclass_pos = find_field_position(headers, "CH Subclass")
    for i in range(0, len(data)):
        if data[i][ch_pos] != '':
            chs = data[i][ch_pos].split(';')
            
            for j in range(0, len(chs)):
                if chs[j] in hash_table_ch and data[i][ch_subclass_pos] not in illegal_cultural_heritage_subclasses:
                    hash_table_ch[chs[j]] += 1
                else: 
                    hash_table_ch[chs[j]] = 1
                
                # followup on animal subclass analysis
                # TODO?

    final_data = [[], []]
    for entry in hash_table_ch:
        final_data[0].append(entry)
        final_data[1].append(hash_table_ch[entry])
        
    save_as_csv(final_data, "cultural_heritage")
    return


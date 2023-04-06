

from config import find_field_position
from file_management import save_as_csv

def prepare_cultural_heritage_data(data):
    '''
    Counts the frequency of different Cultural Heritage enumerations within a given dataset 
    '''
    hash_table_ch = {}
    ch_pos = find_field_position("Culutural Heritage")
    for i in range(0, len(data)):
        if data[i][ch_pos] != '':
            chs = data[i][ch_pos].split(';')
            
            for j in range(0, len(chs)):
                if chs[j] in hash_table_ch:
                    hash_table_ch[chs[j]] += 1
                else: 
                    hash_table_ch[chs[j]] = 1
                
                # followup on animal subclass analysis
                # TODO?

    final_data = []
    for entry in hash_table_ch:
        final_data.append([entry, hash_table_ch[entry]])
        
    save_as_csv(final_data, "cultural_heritage")
    return


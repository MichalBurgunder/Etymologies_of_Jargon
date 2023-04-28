

from config import find_field_position, illegal_cultural_heritage_subclasses, invalid_semantic_numbers
from file_management import save_as_csv

def prepare_cultural_heritage_frequency_total(data, headers):
    """
    Counts the frequency of different Cultural Heritage enumerations within a
    given dataset 
    """
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

def prepare_cultural_heritage_frequency_by_data_set(data, headers, disallowed=[]): 
    hash_table_ds_ch_num = {}
    hash_table_ds_num = {}
    ch_pos = find_field_position(headers, "Cultural Heritage (CH)")
    scrape_ident_pos = find_field_position(headers, "Scrape Identifier")
    sem_num_pos = find_field_position(headers, "Semantic number")
    
    for i in range(0, len(data)):
        # print(str(data[i][scrape_ident_pos]) in disallowed)
        # if (data[i][scrape_ident_pos] in disallowed or # disallowed scrape identifiers, to filter old data sets
        #     str(data[i][sem_num_pos]) in invalid_semantic_numbers) == True:
            # print(str(data[i][sem_num_pos]), invalid_semantic_numbers)
        # print(data[i][sem_num_pos])
        if (data[i][scrape_ident_pos] in disallowed or # disallowed scrape identifiers, to filter old data sets
            str(data[i][sem_num_pos]) in invalid_semantic_numbers): # semantic numbers that mention duplicates
            continue
        
        if data[i][scrape_ident_pos] not in hash_table_ds_ch_num:
            hash_table_ds_ch_num[data[i][scrape_ident_pos]] = 0
            hash_table_ds_num[data[i][scrape_ident_pos]] = 0
            
        if data[i][ch_pos] != '':
            hash_table_ds_ch_num[data[i][scrape_ident_pos]] += 1
        
        hash_table_ds_num[data[i][scrape_ident_pos]] += 1
        
    final_data = [
        hash_table_ds_ch_num.keys(),
        hash_table_ds_ch_num.values(),
        [hash_table_ds_num[ds] for ds in hash_table_ds_ch_num.keys()]
    ]
    save_as_csv(final_data, "cultural_heritage_by_data_set")      
    return
from utils import  find_field_position
from file_management import save_as_csv

def prepare_ety_type_2(data, headers, cs):
    """
    Summarizes all of the 2nd Ety type data into easily anaylzable/graphable data, 
    which it saves to ety_type_2.csv
    """
    print("starting ety type 2 analysis...")
    ety_type_2_pos = find_field_position(headers, "2nd Ety. type")
    
    et2_hm = {
        'Missing': 0
    }

    for i in range(0, len(data)):
        if len(cs['to_analyze']) != 0 and data[i][cs['scrape_identifier_pos']] not in cs['to_analyze']:
            continue
        if data[i][ety_type_2_pos] == '':
            et2_hm['Missing'] += 1
            continue
        if f'{data[i][cs["scrape_identifier_pos"]]}_{data[i][ety_type_2_pos]}' not in et2_hm:
            et2_hm[f'{data[i][cs["scrape_identifier_pos"]]}_{data[i][ety_type_2_pos]}'] = 0
            
        et2_hm[f'{data[i][cs["scrape_identifier_pos"]]}_{data[i][ety_type_2_pos]}'] += 1
    
    
    # we transform the data into a csv
    final_data = []
    for  entry in et2_hm:
        final_data.append([entry, et2_hm[entry]])
        
    save_as_csv(final_data, "ety_type_2")
    return 
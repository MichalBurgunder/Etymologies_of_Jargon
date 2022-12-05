import numpy as np
from utils import  find_field_position

def prepare_ety_type_2(data, headers, cs):
    print("starting ety type 2 analysis...")
    ety_type_2_pos = find_field_position(headers, "Ety. type 2")
    
    et2_hm = {}
    
    for i in range(0, len(data)):
        if data[i][ety_type_2_pos] not in et2_hm[data[i][ety_type_2_pos]]:
            et2_hm[data[i][ety_type_2_pos]] = 0
        et2_hm[data[i][ety_type_2_pos]] += 1
    # print(et2_hm)
    return 
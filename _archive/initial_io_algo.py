
# influence opacity algorithm,
# first version
def go_down(data, entry, cs, count_array, element_pos_hm, leaf_array):
    leaf = True
    for j_pos in cs['jargon_entry_positions']:
        if data[entry][j_pos] != '':
            leaf = False
            count_array[element_pos_hm[data[entry][j_pos]]] += 1 
            element_position = element_pos_hm[data[entry][j_pos]]
            go_down(data, element_position, cs, count_array, element_pos_hm, leaf_array)
    if leaf == True:
        leaf_array[entry] = True
    return

def influence_opacity_algorithm(data, element_pos_hm, cs):
    count_array = [1] * len(data)
    leaf_array = [False] * len(data)
    
    for i in range(0, len(data)):
        go_down(data, i, cs, count_array, element_pos_hm, leaf_array)

    return count_array, leaf_array


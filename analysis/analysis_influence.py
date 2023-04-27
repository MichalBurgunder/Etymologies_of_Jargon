import numpy as np
import sys

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis.utils import find_field_position
from analysis.file_management import save_as_csv
from analysis.utils import concatenate

def pagerank(M, num_iterations: int = 100, d: float = 0.85):
    """
    copied from wikipedia https://en.wikipedia.org/wiki/PageRank
    """
    N = M.shape[1]
    v = np.ones(N) / N
    M_hat = (d * M + (1 - d) / N)
    for i in range(num_iterations):
        v = M_hat @ v
    return v

def is_recursive(data, entry, jargon_poss, ti_hashmap, start_val, recursion_depth=0):
    if recursion_depth == 5: # max recursion depth (max so far is 2)
        return False
    
    new_poss = []

    for j_pos in jargon_poss:
        if data[entry][j_pos] == start_val:
            return (entry, j_pos, data[entry][j_pos])

        if data[entry][j_pos] != '':
            new_poss.append(ti_hashmap[data[entry][j_pos]])
    recursion_depth += 1
    for i in new_poss:
        edge = is_recursive(data, i, jargon_poss, ti_hashmap, start_val, recursion_depth)
        if edge:
            return edge
    recursion_depth -= 1
    return False

def remove_cycles(data, elem_entry_hm, cs):
    removed_edges = []
    for i in range(0, len(data)):
        edge = is_recursive(data, i, cs['jargon_entry_positions'], elem_entry_hm, data[i][cs["clean_name_pos"]])
        if edge:
            data[edge[0]][edge[1]] = ''
            removed_edges.append(edge)
    return removed_edges

def create_pagerank_matrix(data, elem_entry_hm, cs):
    n = len(data)
    the_matrix = [[0] * n for i in range(0, n)]
    edges_removed = remove_cycles(data, elem_entry_hm, cs)

    for i in range(0, len(data)):
        answers = []
        for j in cs['jargon_entry_positions']:
            if data[i][j] != '':
                answers.append(elem_entry_hm[data[i][j]])
        
        
        the_num = len(answers)
        for pos in answers:
            the_matrix[i][pos] = 1/the_num
    
    
    return np.array(the_matrix).T, edges_removed
        

def recursive_influ(matrix, resulting_matrix, i, adder=0):
    # additional_here = 0
    for j in range(0,len(matrix[i])):
        if matrix[i][j] == 1:
            resulting_matrix[j] += 1
            adder += 1
            recursive_influ(matrix, resulting_matrix, j, adder)
            # print(i, additional)
            # additional_here += additional
    # print(additional_here)
    resulting_matrix[i] += adder
    # print(str(resulting_matrix))
    
    # return additional_here + 1
    return 0
    
def influence(matrix):
    n = matrix.shape[0]
    resulting_matrix = np.zeros(n)
    # arrival_matrix = np.zeros((n,n))
    # print(" A  B  C  D  E  F  G  H")
    for i in range(0,len(matrix)):
        recursive_influ(matrix, resulting_matrix, i) 
        
    return resulting_matrix

def nice_results(data, pg_res, submatrix_hm, matrix_master_hm, headers):
    cn_pos = find_field_position(headers, "Cleaned Name")
    keys_of_submatrix = list(submatrix_hm.keys())
    our_tuples = [None for i in range(0, len(pg_res))]
    # print(len(our_tuples))
    # print(len(pg_res))
    # print(len(keys_of_submatrix))
    for i in range(0, len(pg_res)):
        # print(keys_of_submatrix)
        pos_master_matrix = matrix_master_hm[keys_of_submatrix[i]]
        cleaned_name = data[pos_master_matrix][cn_pos]
        our_tuples[i] = (cleaned_name, pg_res[i])
    # our_tuples = [(cleaned_names[i], pg_res[i]) for i in range(len(pg_res))]
    return sorted(our_tuples, key=lambda the_tuple: the_tuple[1], reverse=True)
    
def print_nice_results(res):
    """
    Prints out a latex appropriate text, to easily insert into the final document
    """
    final_data = []
    for i in range(0, len(res)):
        final_data.append([res[i][0], np.round(res[i][1]*(10**14), 2)])
    
    final_string = "\hline\n"
    final_string += f"{final_data[0][0]}"

    for i in range(1, len(final_data)):
        final_string += f" & {final_data[i][0]}"
        
    final_string += " \\\\\n\hline"
    
    final_string += f" \n{final_data[i][1]}"
    
    for i in range(0, len(final_data)):
        final_string += f" & {final_data[i][1]}"
    
    # res = f"\\begin\{tabular\}c\{c\{'|c' * len(final_data)}}"
    final_string += " \\\\\n\hline\n"
    print(final_string)
    
def reinsert_edges(data, edges):
    for i in range(0, len(edges)):
        data[edges[i][0]][edges[i][1]] = edges[i][2]
    return

def fetch_other_jargon(the_hashmap, data, entry, cs, origin_scrape_ident, master_hm):
    jargon_poss = cs['jargon_entry_positions']
    
    for j_pos in jargon_poss:
        the_jargon = data[entry][j_pos]
        if (the_jargon != '' and the_jargon not in the_hashmap[origin_scrape_ident]):
            
            the_hashmap[origin_scrape_ident][the_jargon] = master_hm[the_jargon]
            
            fetch_other_jargon(the_hashmap, data, master_hm[data[entry][j_pos]], cs, origin_scrape_ident, master_hm)
    return

def create_data_set_specific_pg_matrices(data, elem_entry_hm, cs):
    # an array of all different scrape identifiers
    data_sets = list(set(np.array(data)[:,cs["scrape_identifier_pos"]]))
    # data_sets.remove("ADD")
    data_sets.sort() # sorted for deterministic behaviour
    # a hashmap, with n nested hashmaps for each scrape identifier,
    # where the clean name (key) and position in the data array (value) is recorded
    hashmap_datasets_ti = {} 
    
    # here, we set up the hashmap with the different scrape identifiers
    for i in range(0, len(data_sets)):
        hashmap_datasets_ti[data_sets[i]] = {}


    # here, we fill out the each "scrape-identifier data-points set",
    # to get n different hashmaps, from which we can create pageRank matricies
    # we add the scrape identifier data points, and iterate through its jargons, and add these as well
    for i in range(0, len(data)):
        # if data[i][cs['clean_name_pos']] == "library":
        #     print("library is present")
        scrape_ident = data[i][cs['scrape_identifier_pos']]
        clean_name = data[i][cs['clean_name_pos']]
        
        if clean_name not in hashmap_datasets_ti[scrape_ident]:
            hashmap_datasets_ti[scrape_ident][clean_name] = i
            
            fetch_other_jargon(hashmap_datasets_ti, data, i, cs, scrape_ident, elem_entry_hm)

    # print(len(hashmap_datasets_ti['PL'].keys()))
    # exit()
    # now we create the actual matricies. We loop through all possbile submatricies first
    final_matricies = []
    submatrix_hms = []
    for i in range(0, len(data_sets)):
        # print(f"Now doing {data_sets[i]}")
        # we set up for the creation of one submatrix first. We have the count for keys for one data set, but we now just need to find, and create a new hashmap that defines where each point will be in our new submatrix
        the_keys = list(hashmap_datasets_ti[data_sets[i]].keys())
        the_keys.sort()
        # print(the_keys)
        # print(the_keys)
        n = len(the_keys)
        # exit()
        # we define the positions of each point in the submatrix, from the "master-matrix"
        # we do this at the beginning, so that we can always fetch these names in the main "filling-out" loop
        submatrix_hm = {}
        for j in range(0, n):
            submatrix_hm[the_keys[j]] = j 
        # print(submatrix_hm)
        # we FINALLY define the final matrix that will be saved
        pg_matrix = [[0] * n for j in range(0, n)] # actual final pg_submatrix
        
        # now we loop through all of the keys that need to be included in the submatrix
        # in this loop, we find the number that needs to be filled in, as well as the positions where they should be placed
        for j in range(0, n):
            
            # this is the clean name key
            the_key = the_keys[j]
            # we count the number of present jarongs (not ""), and take the reciprocal
            num_jargons = [True if data[elem_entry_hm[the_key]][jargon_pos] != "" else False for jargon_pos in cs['jargon_entry_positions']].count(True)
            if num_jargons == 0:
                continue
            
            # dividend = num_jargons if num_jargons > 0 else 1
            the_num = 1/num_jargons
            # print(the_num)
            # we the num in place, we simply need to fill it in the correct positions in the pg_matrix
            the_check = 0
            for j_pos in cs['jargon_entry_positions']:
                
                # we first find the actual jargon name from the original data set...
                # ...check that its not empty...
                jargon_clean_name = data[elem_entry_hm[the_key]][j_pos]
                if jargon_clean_name != '':
                    # ...before we can fill it in with the help of our submatrix hashmap
                    pg_matrix[submatrix_hm[the_key]][submatrix_hm[jargon_clean_name]] = the_num
                    the_check += 1
               # sum(pg_matrix[submatrix_hm[the_key]]) != 1 or      
            if the_check != num_jargons:
                print("mistake")
                print(sum(pg_matrix[submatrix_hm[the_key]]))
                print(the_check)
                print(the_num)
                print(the_key)
                for j_pos in cs['jargon_entry_positions']:
                    print(data[elem_entry_hm[the_key]][j_pos])
                print()
                exit()
                
        res = np.array(pg_matrix)
        # print(list(np.sum(res, axis=1)))
        print(sum(res[0]))
        # print
        # exit()
        final_matricies.append(np.array(pg_matrix).T)
        submatrix_hms.append(submatrix_hm)
    # print(final_matricies[3])
    return [final_matricies, data_sets, submatrix_hms]

def recursively_find_elements(data, entry, jargon_poss, sub_hm, cs):
    final_array = []
    queue = []
    intermed_hm = {} # to avoid recursive acronyms

                
    return final_array
                

def prepare_influence_data(data, elem_entry_hm, headers, cs):
    # page rank first
    pg_matrix_full, edges_removed = create_pagerank_matrix(data, elem_entry_hm, cs)
    special_matricies, scrape_identifiers, submatrix_hms = create_data_set_specific_pg_matrices(data, elem_entry_hm, cs)
    
    all_pg_matricies = concatenate(special_matricies, [pg_matrix_full])
    all_identifiers = concatenate(scrape_identifiers, ["ALL"])
    all_submatrix_hms = concatenate(submatrix_hms, [elem_entry_hm])
    # ['CP', 'GNU', 'PL', 'PM', 'RG', 'ALL']      ____
    d_values = [0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.4]
    d_values = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
    num_iters = [100, 100, 100, 100, 100, 100, 100]
    print(len(all_pg_matricies))
    for i in range(0, len(all_pg_matricies)):
        pg_res = pagerank(all_pg_matricies[i], d=d_values[i], num_iterations=num_iters[i])
        nice_pg_results = nice_results(data, pg_res, all_submatrix_hms[i], elem_entry_hm, headers)
        save_as_csv(nice_pg_results, f"page_rank_results_{all_identifiers[i]}")
    
    # print_nice_results(nice_pg_results[0:10])
    reinsert_edges(data, edges_removed) # TODO: reinsert this, eventually
    return



# cs = {'jargon_entry_positions': [1,2,3], "clean_name_pos": 0}
# the_hm = {"test1": 0, "test2": 1, "test3": 2}
# matrix = [
#     ["test1", "test2", "",      ""], 
#     ["test2", "",      "",      "test3"], 
#     ["test3", "",      "test1", ""],
# ]

# print(matrix)
# remove_cycles(matrix, the_hm, cs)
# print(matrix)


        
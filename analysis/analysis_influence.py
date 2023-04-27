import numpy as np
import sys

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis.utils import find_field_position
from analysis.file_management import save_as_csv

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

def nice_results(data, pg_res, headers):
    cn_pos = find_field_position(headers, "Cleaned Name")
    cleaned_names = [data[i][cn_pos] for i in range(0, len(data))]
    our_tuples = [(cleaned_names[i], pg_res[i]) for i in range(len(pg_res))]
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

def fetch_other_jargon(the_hashmap, data, entry, cs, origin_scrape_ident):
    print()
    for i in range(0, len(cs['jargon_entry_positions'])):
        print(data[entry][cs['jargon_entry_positions'][i]])
        if (data[entry][cs['jargon_entry_positions'][i]] is not '' and
            data[entry][cs['jargon_entry_positions'][i]] not in the_hashmap[origin_scrape_ident]):
            the_hashmap[origin_scrape_ident][data[i][cs['clean_name_pos']]] = i
            fetch_other_jargon(the_hashmap, data, i, cs, origin_scrape_ident)
    return

def create_data_set_specific_pg_matrices(data, elem_entry_hm, cs):
    # an array of all different scrape identifiers
    data_sets = np.array(list(set(np.array(data)[:,cs["scrape_identifier_pos"]])))
    
    # a hashmap, with n nested hashmaps for each scrape identifier,
    # where the clean name (key) and position in the data array (value) is recorded
    hashmap_datasets_ti = {} 
    
    # here, we set up the hashmap with the different scrape identifiers
    for i in range(0, len(data_sets)):
        hashmap_datasets_ti[data_sets[i]] = {}

    # here, we fill out the each "scrape-identifier data-points set",
    # to get n different hashmaps, from which we can create pageRank matricies
    for i in range(0, len(data)):
        if data[i][cs['clean_name_pos']] not in hashmap_datasets_ti[data[i][cs['scrape_identifier_pos']]]:
            hashmap_datasets_ti[data[i][cs['scrape_identifier_pos']]][data[i][cs['clean_name_pos']]] = i
            fetch_other_jargon(hashmap_datasets_ti, data, i, cs, data[i][cs['scrape_identifier_pos']])

    # now we create the actual matricies. We loop through all possbile submatricies first
    final_matricies = []
    for i in range(0, len(data_sets)):

        # we set up for the creation of one submatrix first. We have the count for keys, but we now just need to find, and create a new hashmap that defines where each point will be in our new submatrix
        the_keys = hashmap_datasets_ti[data_sets[i]].keys()
        n = len(the_keys)

        submatrix_hm = {}
        pg_matrix = [[0] * n for j in range(0, n)]
        for j in range(0, n):
            submatrix_hm[the_keys[j]] = j
            the_key = the_keys[j]
            the_num = 1/len([True if data[elem_entry_hm[the_key]][jargon_pos] != "" else False for jargon_pos in cs['jargon_entry_positions']].count(True))
            
            for j_pos in cs['jargon_entry_positions']:
                jargon_clean_name = data[elem_entry_hm[the_key]][j_pos]
                submatrix_hm[jargon_clean_name] # pos in pg matrix
                pg_matrix[submatrix_hm[the_key]][submatrix_hm[jargon_clean_name]] = the_num
                # jargon_position_subhm = submatrix_hm[the_keys[i]]
                # pg_matrix[entry_pos][jargon_position_subhm] = the_num
            # submatrix_hm[data[queue[0]][cs]["clean_name_pos"]] = pg_pos
            # queue = [j]
            # while(len(queue) > 0):
            #     if data[queue[0]][cs["clean_name_pos"]] not in submatrix_hm:
            #         submatrix_hm[data[queue[0]][cs]["clean_name_pos"]] = pg_pos
            #         pg_pos += 1
                
            #         for j_pos in cs['jargon_entry_positions']:
            #             queue.append(data[j][j_pos])
                    
            #     del queue[0]
        
        
        # now we have a submatrix hashmap, where we know exactly where each elemeent is.
        # we simply need to iterate over the submatrix hashmap, and fill 
        
        for i in range(0, len(the_keys)):
            entry_pos = submatrix_hm[the_keys[i]]
            the_num = 1/len([True if jargon != "" else False for jargon in cs['jargon_entry_positions']].count(True))
            for j_pos in cs['jargon_entry_positions']:
                jargon_position_subhm = submatrix_hm[the_keys[i]]
                pg_matrix[entry_pos][jargon_position_subhm] = the_num
                    
        final_matricies.append(pg_matrix)
        
    return

def recursively_find_elements(data, entry, jargon_poss, sub_hm, cs):
    final_array = []
    queue = []
    intermed_hm = {} # to avoid recursive acronyms

                
    return final_array
                

def prepare_influence_data(data, elem_entry_hm, headers, cs):
    # page rank first
    pg_matrix, edges_removed = create_pagerank_matrix(data, elem_entry_hm, cs)
    special_matricies = create_data_set_specific_pg_matrices(data, elem_entry_hm, cs)
    exit()
    pg_res = pagerank(pg_matrix, d=0.4)
    nice_pg_results = nice_results(data, pg_res, headers)
    save_as_csv(nice_pg_results, "page_rank_results")
    # print(nice_pg_results)
    
    print_nice_results(nice_pg_results[0:10])
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


        
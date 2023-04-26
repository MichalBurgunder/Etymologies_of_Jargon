import numpy as np
import sys

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis.utils import find_field_position

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

def create_pagerank_matrix(data, elem_entry_hm, headers, cs):
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
    for i in range(0, len(res)):
        print(f"{res[i][0]}: {res[i][1]}")
      
def reinsert_edges(data, edges):
    for i in range(0, len(edges)):
        data[edges[i][0]][edges[i][1]] = edges[i][2]
    return

def prepare_influence_data(data, elem_entry_hm, headers, cs):
    # page rank first
    pg_matrix, edges_removed = create_pagerank_matrix(data, elem_entry_hm, headers, cs)
    pg_res = pagerank(pg_matrix, d=0.4)

    nice_pg_results = nice_results(data, pg_res, headers)
    print_nice_results(nice_pg_results[0:10])
    # reinsert_edges(data, edges_removed) # TODO: reinsert this, eventually
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


        
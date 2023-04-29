import numpy as np
import sys

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis.utils import find_field_position
from analysis.file_management import save_as_csv
from analysis.utils import concatenate

def pagerank(M, num_iterations: int = 100, d: float = 0.85):
    """
    A basic implementation of pagerank. Copied from Wikipedia,
    https://en.wikipedia.org/wiki/PageRank
    """
    N = M.shape[1]
    v = np.ones(N) / N
    M_hat = (d * M + (1 - d) / N)
    for i in range(num_iterations):
        v = M_hat @ v
    return v

def is_recursive(data, entry, jargon_poss, ti_hashmap, start_val, recursion_depth=0):
    """
    Performs a DFS on a single entry in a matrix. If any edge is detected that
    brings it back to the starting value, it returns that edge. Otherwise,
    returns fase.
    """
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
    """
    Removes 1 edge from every cycle detected within the data, recursively
    searching the graph in DFS fashion, for every data point.
    """
    removed_edges = []
    for i in range(0, len(data)):
        edge = is_recursive(data, i, cs['jargon_entry_positions'], elem_entry_hm, data[i][cs["clean_name_pos"]])
        if edge:
            data[edge[0]][edge[1]] = ''
            removed_edges.append(edge)
    return removed_edges

def create_pagerank_matrix(data, elem_entry_hm, cs):
    """
    Creates a pagerank matrix, based on some data
    
    Because cycles skew the results in non-sightful way, we remove them prior to
    the creation of the matrix. 
    """
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
        

def nice_results(data, pg_res, submatrix_hm, matrix_master_hm, headers):
    """
    Compiles the results of the pagerank algorithm and returns a list of sorted
    tuples containing 
        name: The name of the data point
        value: the pagerank associated value
        dataset identifier: the scrape identifier of the data point in question)
    """
    cn_pos = find_field_position(headers, "Cleaned Name")
    si_pos = find_field_position(headers, "Scrape Identifier")
    keys_of_submatrix = list(submatrix_hm.keys())
    our_tuples = [None for i in range(0, len(pg_res))]

    for i in range(0, len(pg_res)):
        pos_master_matrix = matrix_master_hm[keys_of_submatrix[i]]
        cleaned_name = data[pos_master_matrix][cn_pos]
        scrape_ident = data[pos_master_matrix][si_pos]
        our_tuples[i] = (cleaned_name, pg_res[i], scrape_ident)

    return sorted(our_tuples, key=lambda the_tuple: the_tuple[1], reverse=True)
    
def reinsert_edges(data, edges):
    """
    Inserts edges (with a specific value) into a graph,
    """
    for i in range(0, len(edges)):
        data[edges[i][0]][edges[i][1]] = edges[i][2]
    return

def fetch_other_jargon(the_hashmap, data, entry, cs, origin_scrape_ident, master_hm):
    """
    Recursively traverses a tree, and inserts the discovered nodes into
    "the_hashmap", with position in the (master) matrix
    """
    jargon_poss = cs['jargon_entry_positions']
    
    for j_pos in jargon_poss:
        the_jargon = data[entry][j_pos]
        if (the_jargon != '' and the_jargon not in the_hashmap[origin_scrape_ident]):
            
            the_hashmap[origin_scrape_ident][the_jargon] = master_hm[the_jargon]
            
            fetch_other_jargon(the_hashmap, data, master_hm[data[entry][j_pos]], cs, origin_scrape_ident, master_hm)
    return

def create_data_set_specific_pg_matrices(data, elem_entry_hm, cs):
    """
    Creates all necessary submatricies and their associated hashmaps in order to
    run pagerank on submatricies of the original (data). Note that each
    submatrix will not only include those data points that have an associated
    scrape identifier, but also all those points that their jargons refer to
    (and their jargons, etc.).
    
    For this reason, find the number of elements in each set by putting the
    names in a hashmap (name: position_in_original_matrix). We construct another
    hashmap per identifier, that maps the keys of the submatrix to a position in
    that submatrix (name: position_in_submatrix). This way, we can run pagerank,
    and eventually reinsert the names for saving data.
    
    The matricies, hashmaps and scrape identifiers are eventually all returned.
    """
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
        scrape_ident = data[i][cs['scrape_identifier_pos']]
        clean_name = data[i][cs['clean_name_pos']]
        
        if clean_name not in hashmap_datasets_ti[scrape_ident]:
            hashmap_datasets_ti[scrape_ident][clean_name] = i
            
            fetch_other_jargon(hashmap_datasets_ti, data, i, cs, scrape_ident, elem_entry_hm)

    # now we create the actual matricies. We loop through all possbile submatricies first
    final_matricies = []
    submatrix_hms = []
    for i in range(0, len(data_sets)):

        # we set up for the creation of one submatrix first. We have the count for keys for one data set, but we now just need to find, and create a new hashmap that defines where each point will be in our new submatrix
        the_keys = list(hashmap_datasets_ti[data_sets[i]].keys())
        the_keys.sort() # was included for determinism

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

            # we the num in place, we simply need to fill it in the correct positions in the pg_matrix
            for j_pos in cs['jargon_entry_positions']:
                
                # we first find the actual jargon name from the original data set...
                # ...check that its not empty...
                jargon_clean_name = data[elem_entry_hm[the_key]][j_pos]
                if jargon_clean_name != '':
                    # ...before we can fill it in with the help of our submatrix hashmap
                    pg_matrix[submatrix_hm[the_key]][submatrix_hm[jargon_clean_name]] = the_num
                
        final_matricies.append(np.array(pg_matrix).T)
        submatrix_hms.append(submatrix_hm)

    return [final_matricies, data_sets, submatrix_hms]
                

def prepare_pagerank_data(data, elem_entry_hm, headers, cs, pg_matricies_only=False):
    """
    Creates all of the data produced by pagerank. If run without
    "pg_matricies_only", it executes pagerank on the incoming data matrix (more
    specifically, its jargons), as well as all of the submatricies that would
    exist if only these data sets were to exist on their own. The number of
    iterations and damping can be specified for each dat set below, although
    I've kept them the same, seeing that it gives ok results. 
    
    With "pg_matricies_only" == True, it only returns all pagerank matricies (1
    of all data, n of submatrices, one for each scrape identifier in cs)
    """
    # page rank first
    pg_matrix_full, edges_removed = create_pagerank_matrix(data, elem_entry_hm, cs)
    special_matricies, scrape_identifiers, submatrix_hms = create_data_set_specific_pg_matrices(data, elem_entry_hm, cs)
    
    all_pg_matricies = concatenate(special_matricies, [pg_matrix_full])
    all_identifiers = concatenate(scrape_identifiers, ["ALL"])
    all_submatrix_hms = concatenate(submatrix_hms, [elem_entry_hm])

    # this is for testing the io algorithm
    # or otherwise, only fetching the matricies for the io algorithm
    if pg_matricies_only:
        # reinsert_edges(data, edges_removed) # we don't reinsert them, just yet
        return [all_pg_matricies, all_identifiers, all_submatrix_hms], edges_removed
    
    d_values = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4] # we do same everywhere
    num_iters = [100, 100, 100, 100, 100, 100, 100] # here too

    for i in range(0, len(all_pg_matricies)):
        pg_res = pagerank(all_pg_matricies[i], d=d_values[i], num_iterations=num_iters[i])
        nice_pg_results = nice_results(data, pg_res, all_submatrix_hms[i], elem_entry_hm, headers)
        save_as_csv(nice_pg_results, f"page_rank_results_{all_identifiers[i]}")
    
    # we've taken out edges to turn the graph into a DAG (instead of a  DAAG)
    # here, we put them back in, in case further processing depends on this
    reinsert_edges(data, edges_removed)
    return all_pg_matricies


def go_down(data, entry, cs, count_array, element_pos_hm, leaf_array):
    """
    The recursive part of the io algorithm. Traverses all paths for every node,
    and increments a node's count upon arrival
    """
    leaf = True
    for i in range(0, len(data[entry])):
        if data[entry][i] != 0:
            leaf = False
            count_array[i] += 1 
            go_down(data, i, cs, count_array, element_pos_hm, leaf_array)
    if leaf == True:
        leaf_array[entry] = True
    return

def influence_opacity_algorithm(data, element_pos_hm, cs):
    """
    The part of the io algorithm tha manages the DFS. The current implementation
    of this subroutine has not been optimized, and needs to be improved at a
    later date, perhaps in its own separate paper/article
    """
    count_array = [1] * len(data)
    leaf_array = [False] * len(data)
    
    for i in range(0, len(data)):
        go_down(data, i, cs, count_array, element_pos_hm, leaf_array)

    return count_array, leaf_array

def reverse_hashmap(hash_map_to_reverse):
    """
    Takes some hashmap and uses its values as keys, and keys as values
    """
    final_map = {}
    items_hm = list(hash_map_to_reverse.items())
    for i in range(0, len(items_hm)):
        final_map[items_hm[i][1]] = items_hm[i][0]
    return final_map
    
def io_algo_wrapper(data, element_pos_hm, cs, og_data):
    """
    This is a wrapper around the DFS-like recursion function. Apart from the
    recursion, the function also sorts things, and eventually saves the
    resulting data.
    """
    # we reverse the existing hashmap.
    # # this way we know what name each index refers to
    pos_to_name_hm = reverse_hashmap(element_pos_hm)


    # we run the io algorithm here
    # first, we calculate influence...
    print("starting io_algorithm (leaf)...")
    count_array_leaf, leaf_array = influence_opacity_algorithm(data.T, element_pos_hm, cs)
    
    #...and second, we calculate opacity
    print("starting io_algorithm (root)...")
    count_array_root, root_array = influence_opacity_algorithm(data, element_pos_hm, cs)

    # we compile the clean names, so we know exactly what index belongs to what name
    clean_names_array = [pos_to_name_hm[i] for i in range(0, len(data))]
    
    # fetch the scrape identifier of the name, i.e. what data set it comes from
    scrp_ient = [og_data[element_pos_hm[clean_names_array[i]]][cs['scrape_identifier_pos']] for i in range(0, len(count_array_leaf))]
    
    # compiling the (near) final results, before we sort
    # this can be done in a lot more elegance, but you know, I'm running of time... 
    # technically, this is still part of the 
    results_leaf = [
        (clean_names_array[i], count_array_leaf[i], leaf_array[i], scrp_ient[i])
                for i in range(0, len(count_array_leaf)) if leaf_array[i] == True]
    results_root = [
        (clean_names_array[i], count_array_root[i], root_array[i], scrp_ient[i])
        for i in range(0, len(count_array_leaf)) if root_array[i] == True]
    
    # now we sort, and we are done
    # technically, this is still part of the io algorithm, although I will
    # elaborate on the algorithm at a later time...
    results_leaf.sort(key=lambda name_val: name_val[1], reverse=True)
    results_root.sort(key=lambda name_val: name_val[1], reverse=True)

    # we save
    save_as_csv(results_leaf, "io_algorithm_max_influence")
    save_as_csv(results_root, "io_algorithm_max_opacity") 
       
    return

import numpy as np
from utils import copy_array
from file_management import save_as_txt, save_as_csv
from config import element_limit, jargon_entries_connection_types_titles, jargon_entries_connection_types_types
from utils import find_field_position
global recur
recur = 0
recur_limit = 20
# The function that computes the max depth of an entry
def get_max_depth(data, entry, element_hashmap, header_hms, cs, previous_jargons, options={}):
    """
    Computes the maximum etymological depth of elements to be analyzed.
    For recursive calls, it only ever computes the depth up to a unique jargon term.
    """
    global recur

    # print('get_max_depth with entry ' + str(data[entry][cs['clean_name_pos']]) + " with depth " + str(len(previous_jargons)))
    if recur == recur_limit:
        print(f"recursion limit reached ({recur_limit})at data_entry {data[entry][cs['clean_name_pos']]}. exiting...")
        exit()
    
    # we take the lower, in order to avoid capitalization disagreements
    # we remove excess whitespace, on either side of the word
    word = data[entry][cs['clean_name_pos']].lower().strip()

    previous_jargons.append(word)
    
    entry = element_hashmap["ti"][word]
    
    max_depths = [-1] # as array, to pass by reference

    if data[entry][header_hms['ti'][cs['ety_depth']]] != "-1": # if the entry has already been computed
        if options['v']:
            print("already computed. Skipping....")
        return data[entry][header_hms['ti'][cs['ety_depth']]]
     
    # for every jargon entry   
    for j_pos in cs['jargon_entry_positions']:
        # if there is no jargon entry, we ignore
        if data[entry][j_pos] == "": 
            continue
        
        # TODO: Why do we return here? Shouldn't it continue checking the other jargons?
        # if the entry is recursive (i.e. it's a term that we've already arrived at), we track its recursion depth and return
        if data[entry][j_pos] in previous_jargons: 
            for i in range(len(previous_jargons), 0, -1):
                if previous_jargons[i-1] == word:
                    return len(previous_jargons)-i
        # TODO: what exactly does this block of code do?
        # if not existing, add to additives (to fix outside of the program) and go to the next jargon entry
        if data[entry][j_pos] not in element_hashmap['ti']:
            if options['v']:
                print(f"Adding new word to additives: {data[entry][j_pos]}")
            cs['additives'].append(data[entry][j_pos])
            continue
        
        # existing. We find it, and populate it like this entry
        row_pos = element_hashmap['ti'][data[entry][j_pos]]
        recur += 1
        prev_jarg = copy_array(previous_jargons)
        
        # we compute the max depth of this particular entry
        max_depth = get_max_depth(data, row_pos, element_hashmap, header_hms, cs, prev_jarg, options)
        # we save the intermediary value for the jargon entry, so that we don't have to compute it multiple times
        data[row_pos][cs['ety_depth_pos']] = max_depth

        recur -= 1
        max_depths.append(max_depth)


    return np.max(max_depths) + 1


def verify_jargon_connection_entries(dataa, cs):
    """
    Verifies that the jargon connection type fields are all present in the enumeration.
    Otherwise, we'd have to include these for the next batch of data. 
    """ 
    jct_poss = []
    jct_hash = {}
    for i in range(0, len(jargon_entries_connection_types_titles)):
        pos = find_field_position(dataa[2], jargon_entries_connection_types_titles[i])
        jct_poss.append(pos)
        jct_hash[pos] = jargon_entries_connection_types_titles[i]
    
    errors = []
    for i in range(0, len(dataa[0])):
        for j in range(0, len(jct_poss)):
            jpos = jct_poss[j]
            dataa[0][i][jpos] = dataa[0][i][jpos].strip()
            if dataa[0][i][jpos-1] != "" and dataa[0][i][jpos] not in jargon_entries_connection_types_types:
                errors.append(f"""Cleaned Name: {dataa[0][i][cs['clean_name_pos']]},\nData Set: {dataa[0][i][cs['scrape_identifier_pos']]},\n{jct_hash[jpos]}: "{dataa[0][i][jpos]}"\n""")
                
    if len(errors) != 0:
        print("Jargon connection types aren't consistent with the enumeration.")
        print("Errors: \n")
        for err in errors:
            print(err)
        print(f"Number of errors: {len(errors)}\nFix the errors, replace the old data and retry, to proceed with analysis")
        exit()
    return

# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

# # computes the etymology depth of any given entry
def populate_ety_depths(dataa, cs, options={}):
    """
    Goes through all inputted jargons and computes the maximum depth of any single
    jargon entry. Additives that have not been included in the data, are saves in
    cs["additives"], so that the user will have the include these in the data next
    time they run the program. Note that because it is essential that these be
    included, the program will exit if even 1 additive that should be present, isn't.
    """
    print('starting ety. depth analysis')
    
    verify_jargon_connection_entries(dataa, cs)
    # import time
    # be = time.time()
    for i in range(1, len(dataa[0])):
        if options['v']:
            print(f"now computing {dataa[0][i][cs['clean_name_pos']]}")
        max_depth = get_max_depth(dataa[0], i, dataa[1], dataa[3], cs, [], options)
        dataa[0][i][cs['ety_depth_pos']] = max_depth
        
        # for debugging purposes
        if i == element_limit:
            print(f"done first {element_limit}")
            print(f"additives: {cs['additives']}")
            save_as_txt(cs['root'], cs['additives'], 'additives')
            exit()
    
    # en = time.time()
    # print(en-be)
        # deduplication of list, for better use
    new_additives = list(set(cs['additives']))

    if len(new_additives):
        print("Additives: \n")
        print(new_additives)
        save_as_csv(new_additives, "new_additives", True, options)
        print("\nAdd new additives to proceed with analysis\n")
        exit()

    return 

def prepare_depth_data(data, cs, headers):
    """
    Assuming that the ety depth data has already been documented, we now
    save the data in a easily readable format for further analysis and graphing, 
    """
    scrape_iden_pos = find_field_position(headers, "Scrape Identifier")
    final_data = []
    for i in range(0, len(data)):
        # we differentiate between a full analysis, and an analysis of only a set of data
        if len(cs['to_analyze']) != 0:
            if data[i][cs["scrape_identifier_pos"]] in cs['to_analyze']:
                final_data.append([data[i][cs["clean_name_pos"]], data[i][cs['ety_depth_pos']], data[i][scrape_iden_pos]])
        else:
            final_data.append([data[i][cs["clean_name_pos"]], data[i][cs['ety_depth_pos']], data[i][scrape_iden_pos]])
    
    save_as_csv(final_data, "ety_depths")


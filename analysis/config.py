from utils import find_field_position

jargon_entries = ["1st Jargon", "2nd Jargon", "3rd Jargon", "4th Jargon"] # the fields which will create our tree
root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data'
raw_data_root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/raw_data'
paths = [
            'Thesis_data - programming_languages.csv', # programming languages (from wikipedia)
            # 'Thesis_data - gnu_software.csv' # gnu software (from wikipedia)
            'Thesis_data - anaconda_packages.csv',
            'Thesis_data - additives.csv', # all additives (entries not originating from scrapes) (from wikipedia)
            # we require that additives be at the end of the array, so that during deduplication, 
            # the additives will be marked as duplicates, and not the original entries
        ]
to_analyze = [
    # 'PL',
    # 'CP',
    # 'GNU'
] # only fill out if you want to the output to include only specific data sets
additives = [] # here will be all the new name additives that have not been added just yet
ety_depth = "Etymology Depth"
clean_name = "Cleaned Name"
scrape_identifier = "Scrape Identifier"
consts = None
debug = False
element_limit = -1
analyzed_data_root = f"{root}/final_data"

# TODO: Need to remove whitespace when data first comes in
def prepare_virtual_fields(dataa, cs):
    cs['ety_depth_pos'] = find_field_position(dataa[1], cs['ety_depth'])
    cs['clean_name_pos'] = find_field_position(dataa[1], cs['clean_name'])
    cs['scrape_name_pos'] = find_field_position(dataa[1], cs['scrape_name'])
    cs['scrape_identifier_pos'] = find_field_position(dataa[1], cs['scrape_identifier_pos'])

def find_jargon_entry_positions(headers, jargons):
    entry_positions = []
    for h in range(0, len(headers)):
        for j in jargons:
            if j == headers[h]:
                entry_positions.append(h)
                break

    if len(entry_positions) != len(jargons):
        print("Can't find jargons. Exiting...")
        exit()
    return entry_positions

def fill_clean_names(dataa, cs):
    for i in range(0, len(dataa[0])):
        if dataa[0][i][cs['clean_name_pos']] == '':
            dataa[0][i][cs['clean_name_pos']] = dataa[0][i][cs['scrape_name_pos']]
    
    
def prepare_globals(dataa):
    global consts
    
    consts = {
        'jargon_entries': jargon_entries, # the fields which will create our tree
        'jargon_entry_positions': None,
        'root': root,
        'raw_data_root': raw_data_root,
        'paths': paths,
        'to_analyze': to_analyze,
        'additives': [], # here will be all the new name additives that have not been added just ye
        'virtual_fields': ["ety.depth"],
        'vf_default_values': ['-1'],
        'clean_name': "Cleaned Name",
        'clean_name_pos': None,
        'scrape_name': 'Scrape Name', 
        'ety_depth': "Etymology Depth",
        'ety_depth_pos': None,
        'analyzed_data_root': analyzed_data_root,
        'scrape_identifier_pos': 'Scrape Identifier',
        'to_analyze': to_analyze
    }

    # lets find the jargon entry positions
    consts['jargon_entry_positions'] = find_jargon_entry_positions(dataa[1], consts['jargon_entries'])

    prepare_virtual_fields(dataa, consts)

    return consts
jargon_entries = ["1st Jargon", "2nd Jargon", "3rd Jargon", "4th Jargon"] # the fields which will create our tree
root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data'
paths = [
            'programming_languages.csv', # programming languages
            'additives.csv'
        ]

additives = [] # here will be all the new name additives that have not been added just yet


#  root, paths, ety_depth
ety_depth = "Etymology Depth"
# ety_depth_pos = None
clean_name = "Cleaned Name"

# virtual_fields = ["ety.depth"]
# vf_default_values = ['-1']

# clean_name_pos = None

consts = None

def find_field_position(headers, field):
    for i in range(0,len(headers)):
        if headers[i] == field:
            print(field)
            print(i)
            return i
    raise f"Cannot find '{field}' column"

def prepare_virtual_fields(dataa, cs):
    cs['ety_depth_pos'] = find_field_position(dataa[2], cs['ety_depth'])
    cs['clean_name_pos'] = find_field_position(dataa[2], cs['clean_name'])
    cs['scrape_name_pos'] = find_field_position(dataa[2], cs['clean_name'])

def find_jargon_entry_positions(headers, jargons):
    entry_positions = []
    for h in range(0, len(headers)):
        for j in jargons:
            if j == headers[h]:
                entry_positions.append(h)
                break

    if len(entry_positions) != len(jargons):
        print("cant find jargons")
        exit()
    return entry_positions

def fill_clean_names(dataa, cs):
    for i in range(0, len(dataa[0])):
        if dataa[0][i][cs['clean_name_pos']] == '':
            print(dataa[0][i][cs['clean_name_pos']])
            print(dataa[0][i][cs['scrape_name_pos']])
            dataa[0][i][cs['clean_name_pos']] = dataa[0][i][cs['scrape_name_pos']] 
            print(dataa[0][i][cs['clean_name_pos']])
            exit()
    
    
def prepare_globals(dataa):
    global consts
    
    print("?")
    consts = {
        'jargon_entries': jargon_entries, # the fields which will create our tree
        'jargon_entry_positions': None,
        'root': '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data',
        'paths': [
                    'programming_languages.csv', # programming languages
                    'additives.csv' # all additives
                ],
        'additives': [], # here will be all the new name additives that have not been added just ye
        'virtual_fields': ["ety.depth"],
        'vf_default_values': ['-1'],
        'clean_name': "Cleaned Name",
        'clean_name_pos': None,
        
        'ety_depth': "Etymology Depth",
        'ety_depth_pos': None,
    }

    # lets find the jargon entry positions
    consts['jargon_entry_positions'] = find_jargon_entry_positions(dataa[2], consts['jargon_entries'])

        
        
    prepare_virtual_fields(dataa, consts)

    return consts
    


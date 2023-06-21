from analysis.utils import find_field_position

jargon_entries = ["1st Jargon", "2nd Jargon", "3rd Jargon", "4th Jargon"] # the fields which will create our etymological tree
jargon_entries_connection_types_titles = [the_string + " Connection Type" for the_string in jargon_entries] # the descriptions of the connection between jargons 
jargon_entries_connection_types_types = [
        "Attribution",
        "Theme",
        "Version",
        "Reference",
        "Abbr. Reference",
        "Exact Reference",
        "Implicit"
    ] # an enum of what jargon connection types we accept
root = '/Users/michal/Documents/thesis/etymologies_of_jargon'
raw_data_root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/raw_data'
paths = [
            'Thesis_data - programming_languages.csv', # programming languages (from wikipedia)
            'Thesis_data - gnu_software.csv', # gnu software (from wikipedia)
            'Thesis_data - anaconda_packages.csv',
            'Thesis_data - sampled_gems.csv', # ruby gems (sampled with 'gem' command)
            'Thesis_data - package_managers.csv', # package managers (from wikipedia)
            'Thesis_data - additives.csv', # all additives (entries not originating from scrapes) (from wikipedia)
            # we require that additives be at the end of the array, so that during deduplication, 
            # the additives will be marked as duplicates, and not the original entries
            # if the additive seems to be a duplicate, one can find the other entry by moving the additive file name to the top
        ]
to_analyze = [
    # 'PL',
    # 'CP',
    # 'GNU'
] # only fill out if you want to the output to include only specific data sets

invalid_semantic_numbers = ['2','3','9', '10']
additives = [] # here will be all the new name additives that have not been added just yet
ety_depth = "Etymology Depth"
clean_name = "Cleaned Name"
scrape_identifier = "Scrape Identifier"
consts = None # placeholder to define the scope
debug = False # in the end, this doesn't do much
element_limit = -1 # -1 means no limit as to how much data we should process
analyzed_data_root = f"{root}/final_data"
illegal_cultural_heritage_subclasses = ["Logo"]
file_names = {
    "morpheme": "number_morphemes_",
    "ety_type_2": "ety_type_2_frequencies_",
    "name_length": "name_length_",
    "CH": "cultural_heritage",
}

# taken from https://spectrum.ieee.org/top-programming-languages-2022, (spectrum)
top_languages = [name.lower() for name in ["Python", "C", "C++", "C#", "Java", "SQL", "JavaScript", "R", "HTML", "TypeScript", "Go", "PHP", "Shell", "Ruby", "Scala", "Matlab", "SAS", "ASM", "Kotlin", "Rust", "Perl", "Objective-C", "Dart", "Swift", "Verilog", "Arduino", "D", "Julia", "Cuda", "VHDL", "Visual Basic", "LabView", "Groovy", "Lua", "Ada", "Scheme", "ABAP", "Haskell", "COBOL", "Elixir", "F#", "LISP", "Pascal", "FORTRAN", "TCL", "Clojure", "Prolog", "Ocaml", "Ladder Logic", "Erlang", "J", "Forth", "Elm", "Raku", "WebAssembly", "CoffeeScript", "Eiffel"]]

def prepare_cs_fields(dataa, cs):
    """
    Creates virtual fields in constants, for constant time variable lookup
    """
    cs['ety_depth_pos'] = find_field_position(dataa[1], cs['ety_depth'])
    cs['clean_name_pos'] = find_field_position(dataa[1], cs['clean_name'])
    cs['scrape_name_pos'] = find_field_position(dataa[1], cs['scrape_name'])
    cs['scrape_identifier_pos'] = find_field_position(dataa[1], cs['scrape_identifier_pos'])

def find_jargon_entry_positions(headers, jargons):
    """
    Finds the positions of the "\# Jargon" fields in the headers,
    and returns their positions in the array
    """
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

# fills out missing clean name column entries.
# By default, those that are empty, are simply the scrape name
def fill_clean_names(dataa, cs):
    """
    For a given data set, fills out the "Cleaned Name" column with the "Scrape Name"
    field, if it is not already filled out
    """
    for i in range(0, len(dataa[0])):
        if dataa[0][i][cs['clean_name_pos']] == '':
            dataa[0][i][cs['clean_name_pos']] = dataa[0][i][cs['scrape_name_pos']]
            # we defualt bring it to lower here, as we are looping through all data
        #     dataa[0][i][cs['clean_name_pos']] = dataa[0][i][cs['scrape_name_pos']].lower()
        # else:
        #      dataa[0][i][cs['clean_name_pos']] = dataa[0][i][cs['clean_name_pos']].lower()
    
    
def prepare_globals(dataa):
    """
    Creates the constants hashmap for constant time lookups of key variables
    """
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
        'scrape_name_pos': None,
        'ety_depth': "Etymology Depth",
        'ety_depth_pos': None,
        'analyzed_data_root': analyzed_data_root,
        'scrape_identifier_pos': 'Scrape Identifier',
        'to_analyze': to_analyze
    }

    # lets find the jargon entry positions
    consts['jargon_entry_positions'] = find_jargon_entry_positions(dataa[1], consts['jargon_entries'])

    prepare_cs_fields(dataa, consts)

    return consts
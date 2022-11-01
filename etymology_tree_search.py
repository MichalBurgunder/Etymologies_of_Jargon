import csv
from re import I
import pandas as pd
from os import system
import time

system('clear')

def get_header_hashmaps(headers):
    head_i_hm = {}
    i_head_hm = {}
    
    for i in range(0,len(headers)):
        i_head_hm[i] = headers[i]
        head_i_hm[headers[i]] = i
    return {"it": i_head_hm, "ti": head_i_hm}
      
def find_clean_name_position(headers):
    for i in range(0,len(headers)):
        if headers[i] == "Cleaned Name":
            return i
    raise "Cannot find 'Cleaned Name' column"

    
def prepare_data(path):
    all_elements = []
    element_hash_map = {}
    file = csv.reader(open(path, mode ='r'))
    headers = next(file)
    header_hms = get_header_hashmaps(headers)
    clean_name_pos = find_clean_name_position(headers)

    i = 1
    for line in file:
        all_elements.append(line)
        element_hash_map[line[clean_name_pos]] = i
        i += 1

    return all_elements, element_hash_map, headers, header_hms

def add_virtual_columns(data_sets, headerss, hm, name, default_value):
    for i in range(0,len(headerss)):
        headerss[i].append(name)
    
    for i in range(0,len(data_sets)):
        for j in range(0,headerss[i]):
            data_sets[i][j].append(default_value)
        new_data <- cbind(all_data, ety.depth = -1)
        return(new_data)
}
# programming languages
pls_liness, pls_element_hash_map, pls_headers, pls_header_hms = prepare_data('/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/programming_languages.csv')
# any other jargons that don't fit in any other of the data sets
additives_liness, additive_helement_hash_map, additive_headers, additive_hheader_hms = prepare_data('/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/programming_languages.csv')
# ...

additives = [] # here will be all the new name additives that have not been added just yet

jargon_entries = ["X1st Jargon", "X2nd Jargon", "X3rd Jargon", "X4th Jargon"] # the fields which will create our tree

ety_depth = "Etymology Depth"
clean_name = "Cleaned Name"


# this is the function that computes all etymology depths, for all dat sets
def compute_all_depth(dataa):
    
    for (i in 1:nrow(data)) {
        if(i %% 40 == 0) {
            print(sprintf("computing entry %d", i))
        }
        if(i==100) {
            return()
        }
        # new <- data.frame(name=data[i,"Cleaned.Name"])
        data <- populate_depths(data, i)


# # finds the entry number of the jargon file in question
# # if jargon can't be found, simply returns the word
# find_location_jargon <- function(data_frame, word) {
#     for (i in 1:nrow(data_frame)) {     
#         if (all_data[i,][clean_name] == word) {
#             return(i)
#         }
#     }
#     return(-1)
# }

# check_if_recursive <- function(names_found, current_name) {
#     for(i in 1:nrow(names_found)) {
#         # print("hi")
#         # print(names_found)
#         # print(current_name)
#         if(names_found[i,] == current_name) {
#             # print("??")
#             return(0)
#         }
#     }
#     return(-1)
# }
# # checks if a variable is an integer
# is_integer <- function(x) {
#     return(grepl("^[0-9]{1,}$", x=x))
# }
# # computes the etymology depth of any given entry
# populate_depths <- function(data_frame, entry, found_names=data.frame(name=data_frame[entry,"Cleaned.Name"])) {
#     # we add things to our names list, so that if there is a recursive entry, we can handle it
#     # print(found_names)
#     # q()
    
    
#     # i = 63
#     final_number <- -1 # denotes an entry that hasn't been checked yet

#     # print(length((jargon_entries)))
#     for (i in 1:length((jargon_entries))) {
#         # print(data_frame[i, "Cleaned.Name"])
#         # print(i)
#         # print(data_frame[entry,][jargon_entries[i]])
#         if (data_frame[entry,][jargon_entries[i]] != "") {
#             # print("here")
#             # jargon word has been found. Therefore, we need to go into it,
#             # and find the depth of this jargon
#             # print("made it here")
#             jargon_entry <- find_location_jargon(data_frame, all_data[entry,][jargon_entries[i]])
#             print(jargon_entry)
#             # if(data_frame[i, "Cleaned.Name"] != "BlooP" & data_frame[i, "Cleaned.Name"] != "FlooP") {
#             # # print("in here")
#             #     next
#             # }
#             if(jargon_entry == -1) {
#                 rbind(new_additives, all_data[jargon_entry,])
#                 next
#             }

#             print("lalla")
#             # check if it is a name we have already found
#             if(check_if_recursive(found_names, all_data[entry,"Cleaned.Name"]) != -1) {
#                 # print("here")
#                 # have already found it. We make sure it isn't another branch
#                 if(data_frame[entry,][etymology_depth] == -1) {
#                      data_frame[entry,][etymology_depth] <- 0
#                 }
               
#                 return(data_frame[entry,])
#             }

#             print("made it")
#             # print(data_frame[jargon_entry,"Cleaned.Name"])
#             # print(found_names)
#             new_entry <-  data.frame(name=data_frame[jargon_entry,"Cleaned.Name"])
#             found_names <- rbind(found_names,new_entry)
#             # print(found_names)
#             # q()
#             max_depth <- populate_depths(data_frame, jargon_entry, found_names)
            
#             if(max_depth["ety.depth"] > final_number) {
#                 final_number <- max_depth["ety.depth"]
#             }

#         }

#     }

#     print("test")
#     data_frame[entry,][etymology_depth] <- final_number + 1

 
#     return(data_frame)
# }

# all_raw_data <- rbind(pls)

# all_data <- add_virtual_columns(all_raw_data)




# entry <- 63
# # print(all_data[entry,]["Cleaned.Name"])
# # print(all_data[entry,]["Cleaned.Name"])
# print("outside")
# # print(all_data)
# # q()
# res <- populate_depths(all_data, entry, found_names=data.frame(name=all_data[entry,"Cleaned.Name"]))
# # print(all_data[c("Cleaned.Name", "ety.depth")])
# # res <- compute_all_depths(all_data)

# # print(new_additives)
# r <- "end"
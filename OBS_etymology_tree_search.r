

# HERE ALL THE DATA SETS THAT WE ARE IMPORTING FOR ANALYSIS

# programming languages
pls <- read.csv("/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/programming_languages.csv", header = TRUE, stringsAsFactors = FALSE)

# any other jargons that don't fit in any other of the data sets
additives <- read.csv("/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/programming_languages.csv", header = TRUE, stringsAsFactors = FALSE)
# ...

# ALL THE OTHER GLOBALS

etymology_depth <- "ety.depth"
clean_name <- "Cleaned.Name"

jargon_entries <- array(0, c(4, 1))

jargon_entries[1] <- "X1st.Jargon"
jargon_entries[2] <- "X2nd.Jargon"
jargon_entries[3] <- "X3rd.Jargon"
jargon_entries[4] <- "X4th.Jargon"

# here we add all new jargon terms to manually add
new_additives <- array(0, c(0, 1))


# adds virtual columns to the data, which are used for computation sake
add_virtual_columns <- function(all_data) {
    new_data <- cbind(all_data, ety.depth = -1)
    return(new_data)
}
# this is the function that computes all etymology depths, for all dat sets
compute_all_depths <- function(data) {
    for (i in 1:nrow(data)) {
        if(i %% 40 == 0) {
            print(sprintf("computing entry %d", i))
        }
        if(i==100) {
            return()
        }
        # new <- data.frame(name=data[i,"Cleaned.Name"])
        data <- populate_depths(data, i)

    }
}


# finds the entry number of the jargon file in question
# if jargon can't be found, simply returns the word
find_location_jargon <- function(data_frame, word) {
    for (i in 1:nrow(data_frame)) {     
        if (all_data[i,][clean_name] == word) {
            return(i)
        }
    }
    return(-1)
}

check_if_recursive <- function(names_found, current_name) {
    for(i in 1:nrow(names_found)) {
        # print("hi")
        # print(names_found)
        # print(current_name)
        if(names_found[i,] == current_name) {
            # print("??")
            return(0)
        }
    }
    return(-1)
}
# checks if a variable is an integer
is_integer <- function(x) {
    return(grepl("^[0-9]{1,}$", x=x))
}
# computes the etymology depth of any given entry
populate_depths <- function(data_frame, entry, found_names=data.frame(name=data_frame[entry,"Cleaned.Name"])) {
    # we add things to our names list, so that if there is a recursive entry, we can handle it
    # print(found_names)
    # q()
    
    
    # i = 63
    final_number <- -1 # denotes an entry that hasn't been checked yet

    # print(length((jargon_entries)))
    for (i in 1:length((jargon_entries))) {
        # print(data_frame[i, "Cleaned.Name"])
        # print(i)
        # print(data_frame[entry,][jargon_entries[i]])
        if (data_frame[entry,][jargon_entries[i]] != "") {
            # print("here")
            # jargon word has been found. Therefore, we need to go into it,
            # and find the depth of this jargon
            # print("made it here")
            jargon_entry <- find_location_jargon(data_frame, all_data[entry,][jargon_entries[i]])
            print(jargon_entry)
            # if(data_frame[i, "Cleaned.Name"] != "BlooP" & data_frame[i, "Cleaned.Name"] != "FlooP") {
            # # print("in here")
            #     next
            # }
            if(jargon_entry == -1) {
                rbind(new_additives, all_data[jargon_entry,])
                next
            }

            print("lalla")
            # check if it is a name we have already found
            if(check_if_recursive(found_names, all_data[entry,"Cleaned.Name"]) != -1) {
                # print("here")
                # have already found it. We make sure it isn't another branch
                if(data_frame[entry,][etymology_depth] == -1) {
                     data_frame[entry,][etymology_depth] <- 0
                }
               
                return(data_frame[entry,])
            }

            print("made it")
            # print(data_frame[jargon_entry,"Cleaned.Name"])
            # print(found_names)
            new_entry <-  data.frame(name=data_frame[jargon_entry,"Cleaned.Name"])
            found_names <- rbind(found_names,new_entry)
            # print(found_names)
            # q()
            max_depth <- populate_depths(data_frame, jargon_entry, found_names)
            
            if(max_depth["ety.depth"] > final_number) {
                final_number <- max_depth["ety.depth"]
            }

        }

    }

    print("test")
    data_frame[entry,][etymology_depth] <- final_number + 1

 
    return(data_frame)
}

all_raw_data <- rbind(pls)

all_data <- add_virtual_columns(all_raw_data)




entry <- 63
# print(all_data[entry,]["Cleaned.Name"])
# print(all_data[entry,]["Cleaned.Name"])
print("outside")
# print(all_data)
# q()
res <- populate_depths(all_data, entry, found_names=data.frame(name=all_data[entry,"Cleaned.Name"]))
# print(all_data[c("Cleaned.Name", "ety.depth")])
# res <- compute_all_depths(all_data)

# print(new_additives)
r <- "end"
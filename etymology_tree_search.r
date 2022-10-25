

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
        populate_depths(data, i, TRUE)

    }
}


# finds the entry number of the jargon file in question
# if jargon can't be found, simply returns the word
find_location_jargon <- function(data_frame, word) {
    for (i in 1:length(data_frame)) {
        if (all_data[i,][clean_name] == word) {
            return(i)
        }
    }
    return(-1)
}

# checks if a variable is an integer
is_integer <- function(x) {
    return(grepl("^[0-9]{1,}$", x=x))
}
# computes the etymology depth of any given entry
populate_depths <- function(data_frame, entry, first=FALSE) {
    # if (data_frame[entry,][etymology_depth] != -1) {
    #     # already done. We go back
    #     return(data_frame[entry,][etymology_depth])
    # }

    final_number <- -1 # denotes an entry that hasn't been checked yet

    for (i in 1:length((jargon_entries))) {
        # check to see if we need to go in, in the first place
        # if(i == 10 && first == TRUE) {
        #     break
        # }
   
        if (data_frame[entry,][jargon_entries[i]] != "") {
            # jargon word has been found. Therefore, we need to go into it,
            # and find the depth of this jargon
            jargon_entry <- find_location_jargon(data_frame, all_data[entry,][jargon_entries[i]])

            if(jargon_entry == -1) {
                rbind(new_additives, all_data[jargon_entry,])
                next
            }
            
            max_depth <- populate_depths(data_frame, jargon_entry)
            
            if(max_depth > final_number) {
                final_number <- max_depth
            }

        }

    }
    
    data_frame[entry,][etymology_depth] <- final_number + 1
    
 
    return(data_frame[entry,][etymology_depth])
}

all_raw_data <- rbind(pls)

all_data <- add_virtual_columns(all_raw_data)


entry <- 101
# print(all_data[entry,]["Cleaned.Name"])
res <- populate_depths(all_data, entry)
# q()
# r <- "test"
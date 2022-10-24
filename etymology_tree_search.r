

pls <- read.csv("/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/programming_languages.csv", header=TRUE, stringsAsFactors=FALSE)
# ...

pls_depth_per_entry <- array(0, c(nrow(pls),1))
# ...

all_data = c(pls_depth_per_entry, )

jargon_entries <- array(0, c(4,1))
jargon_entries[1] <- "1st Jargon"
jargon_entries[2] <- "2nd Jargon"
jargon_entries[3] <- "3rd Jargon"
jargon_entries[4] <- "4th Jargon"

# this is the function that computes all etymology depths, for all dat sets
compute_all_depths <- function(data) {
    for(i in 1:length(all_data)) {
        populate_depths(all_data[i])
    }
}
# this is the function to call, when trying to determine the etymology depth of any given data set
populate_depths <- function(data_frame) {
    for(i in 1:nrow(data_frame)) {       # for-loop over rows
        if(depth_per_entry[i] == 0) {
            depth[i] <- etymology_depth(pls, i)
        }
    }
}

# finds the entry number of the jargon file in question
# if jargon can't be found, simply returns the word
find_location_jargon <- function(word) {

}

# checks if a variable is an integer
is_integer <- function)() {
    return(grepl("^[0-9]{1,}$", ))
}
# computes the etymology depth of any given entry
etymology_depth <- function(pls, i) {
    final_number <- 0

    for(j in 1:length(jargon_entries)) {
        # check to see if we need to go in, in the first place
        if(pls[,i][j] != '') { 
            loc_jar1 <- find_location_jargon(pls[,i]["1st Jargon"])
            if(is_integer(loc_jar1)) {
                final_number = final_number + loc_jar1
            } else {

            }
    }
    }


}


compute_all_depths()
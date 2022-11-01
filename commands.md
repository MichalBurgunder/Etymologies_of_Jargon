# read csv

pls <- read.csv("/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/programming_languages.csv", header=TRUE, stringsAsFactors=FALSE)

# Get all animal data

<!-- pls[pls$Duplicate==''&pls$Semantic.number==1&pls$Cultural.Heritage=='Animal', c(5,9,11,13,14,21)] -->
pls[pls$Duplicate==''&pls$Semantic.number==1&pls$Cultural.Heritage=='Animal', c("Cleaned.Name","Year","Ety..type","Etymology","Full.Expansion.Phrase","Cultural.Heritage")]

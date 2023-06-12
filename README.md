# onomastiware (Onomastics of Software)

This repository is published in conjunction with the hand-in of my Master's thesis "Onomastics of Software". It is primarily meant as an addtional source of information for the Master's committee, who are evaluating my handed in thesis (see `latex/main.tex` for the full latex text for the thesis.). It's secondary use, is for any researchers who might be interested in either creating & analyzing their own data sets, or researchers who would like to build on on this thesis, to either perform more analyses, extend data sets, or use this repo for any other endeavor they might have.  

## Analyses

**Name Length**: Counts the length of the names inserted
**Morpheme Count**: Counts the number of morphemes per node
**Maximum Depth**: Computes the maximum depth of a single node
**Ety_type 1**: Creates a histogram of Ety. types by decade
**Ety_type 2**: Does the same thing as the above anaylsis, but instead, with the 2nd "Ety. Type" field
**Power Iteration**: Computes the power iteration values for each node, on the whole inserted data set, or on a dataset with a particular identifier
**Influence & Opacity**: Computes the *influence* and *opacity* of a node


## Usage

While the software can recreate the proessed data & tables, its most useful feature is that you can add your own data sets into the software, and perform the same analyses that I have, with my own data.

1. Copy all metadata fields from one of the initial data sets that I have pushed so far, and copy them into your own spreadsheet (or .csv, if you're a psychopath).
2. Fill out the spreadsheet, adding the names you want to include in your analysis. For this step, __only__ fill out the "Scrape Name" field.
3. In `analysis/config.py`, add your file name to the 'paths' variable. Place it in the zeros (first) position.
4. Convert your spreadsheet into a .csv file (if you're psychotic, it should already be in .csv format) and place it into `thesis_data/raw_data`
5. Run the analysis with this still empty data set, by executing `python analysis/main.py`. This should check for duplicates between your data set and the other data sets. If duplicates are found, you have 2 options: (1), while the name is the same, the already present object is a different object than yours. Add a " (your_data_set_name)" to your data point, or (2), you remove your data point from the analysis. Currently, we do not support more sophisticate way of dealing with duplicate names. 
6. Once there are no duplicates, fill out your entire table. If there are critical mistakes, the software should catch it. Otherwise, you will clearly see the mistakes when you visualize your data
7. Uncomment all functions in `analysis/main.py` underneath "ACTUAL ANALYSIS" that you wish to run. Add your own data sets analyses by adding the appropriate functions with your unique scrape identifier
8. Run `python analysis/main.py`. This will create all the data you specified.
9. Modify the `visualization.py` file, to specify which data sets should be visualized
10. Run `python visualization.py`. You will find your figures in `figures`

## Licence

All of this software and its data is licensed under the MIT licence. The reason for this, is that while I would like all applicaton to be open source as well (GPL), I'd more like for people to do whatever they want with the data provided. The study has (in a vague shape or form) been funded by the Università della svizzera italiana (USI), a institution funded by the state, so the the products of the university ought to "belong" to the state, i.e. everyone in the country, and so, the world.

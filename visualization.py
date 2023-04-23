import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import sys  
import random 
import os     
import random 

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon/analysis')
from analysis.file_management import read_csv, save_as_csv
from analysis.config import file_names
from analysis.utils import concatenate

os.system('clear')

root = '/Users/michal/Documents/thesis/etymologies_of_jargon/results'

def create_bar_graph_log_subplots(ys, xs, info):
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 2))
    
    # bar graph
    ax1.bar(xs, ys, color='navy')
    ax1.set_yscale('linear')
    ax1.set_title('counts')
    ax1.set_xlabel("Depths")
    ax1.set_ylabel("Frequency")
    ax1.set_xticks(range(0, len(xs)))
    
    # log line, with scatter
    ax2.scatter(xs, ys, color='navy')
    ax2.plot(xs, ys, color='navy')
    ax2.set_yscale('log')
    ax2.set_title('counts log scale')
    ax2.set_xlabel("Depths")
    ax2.set_ylabel("Frequency")

    fig.suptitle(f"Max. Etymological Depth {info['data_set']}")
    fig.savefig(f"figures/bar_graph_max_ety_depth_{info['data_set']}.png", bbox_inches='tight')

    return

def create_bar_graph(ys, xs, info, log=False):
    """
    Creates a simple bar graphs, given the appropriate inputs.
    'info' is a dictionary consisting of 'xlabel', 'ylabel' and 'title'.
    Skipping any of these parameters will cause an error
    """
    # fig = plt.figure()
    
    # plt.xlabel(info["xlabel"])
    # plt.ylabel(info["ylabel"])
    # plt.title(info["title"])
    
    # the bar plot
    if not log:
        plt.bar(xs, ys, color ='navy',
            width = 0.4)
        plt.show()
        return
    
    # linear
    plt.subplot(221)
    plt.bar(xs, ys, color ='navy',)
    plt.yscale('linear')
    plt.title('linear')
    # plt.grid(True)

    # log
    plt.subplot(222)
    plt.plot(xs, ys)
    plt.yscale('log')
    plt.title('log')
    # plt.grid(True)
    # plt.show()
    plt.savefig(f"figures/bar_graph_ety_depths_{info['set']}.png", bbox_inches='tight')
    plt.clf()
    return
   
def number_of_depths(file_name, data_set='ALL'):
    """
    Creates a bar graph/histogram with all the etymological depths of a specific file
    """
    rows = read_csv(file_name)
    nums = [] # position of where the depth is located
    max_value = 0
    for row in rows:
        max_value = max(max_value, int(row[1]))
        if data_set == 'ALL' or row[2] == data_set:
            nums.append(int(row[1]))
    
    bars = [nums.count(i) for i in range(0, max_value+1+1)] # +1 to add the last one, +1 to signify the end

    info = {
        "xlabel": "Occurences",
        "ylabel": "No. of Etymology Depths",
        "data_set": data_set
    }
    return create_bar_graph_log_subplots(list(bars), list(range(0, len(bars))), info)

def convert_to_ints(data):
    """
    Converts an array of stringified integers to integers
    """
    for i in range(0,len(data)):
        for j in range(0,len(data[i])):
            data[i][j] = int(data[i][j])
    return np.array(data)
        
def order_data_by_frequency(data, old_rows):
    """
    Orders an array of arrays by the sum of the (inner) array.
    Used to display the stacked barchart, with the most significant
    bars displayed at the bottom
    """
    sorted_sums = sorted([(sum(data[i]), i) for i in range(0,len(data))])
    sorted_sums.reverse()
    
    sorted_data = []
    new_rows = []
    for i in range(0, len(data)):
        sorted_data.append(data[sorted_sums[i][1]])
        new_rows.append(old_rows[sorted_sums[i][1]])

    return sorted_data, new_rows

def linify(data):
    """
    Adds a line line for label headings so that they are easily readable
    """
    return [data[i].replace('-','-\n')for i in range(0, len(data))]

def normalize_data(data):
    """
    Normalizes the data to a standard of 100, so that ety types can be compared over the decades
    """
    sums = np.array(data, dtype=np.double).sum(axis=0)

    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if sums[j] != 0:
                data[i][j] = data[i][j]/sums[j]*100
    
    return np.array(data)

def ety_types(filename, normalized=False):
    data_csv = read_csv(filename)
    columns = linify(data_csv[0]) # fetching columns
    rows = data_csv[-1] # fetching rows
    dtype_data = np.double if normalized else np.int16
    data = np.array(data_csv[1:len(data_csv)-1],dtype=dtype_data)
    data = convert_to_ints(data)
    data, rows = order_data_by_frequency(data, rows)

    if normalized:
        data = normalize_data(data)
        save_as_csv(np.round(data, 1), "temp_normalized_ety_types")

    colors = plt.cm.tab20((4./3*np.arange(len(rows))).astype(int))

    n_rows = len(data)
    
    fig, ax = plt.subplots(num=None, figsize=(12, 12), dpi=80, facecolor='w', edgecolor='k')
    
    # plot the bars + text labels
    cell_text = []
    bottoms = None
    for row in range(0,n_rows):
        bottoms = [0]*len(columns) if row == 0 else bottoms + data[row-1]
        # plt.bar(columns, data[row], width=bar_width, bottom=bottoms, color=colors[row], align='center')
        print(columns)
        print(data[row])
        plt.bar(columns, data[row], color=colors[row],  bottom=bottoms, align='center')
        # exit()
        cell_text.append(data[row])
        
    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.5)
    plt.legend(rows, loc='upper left')
    # plt.subplot(figsize=(16, 12))

    # plt.ylabel("Loss in ${0}'s".format(value_increment))
    # plt.yticks(values * value_increment, ['%d' % val for val in values])
    # plt.xticks([])
    # plt.set_xticklabels(ticks=columns)
    normalization_extension_title = ' - Normalized' if normalized else ''
    normalization_extension_fig_name = '_normalized' if normalized else ''
    ety_version_title = "1st" if "1" in filename else "2nd" # to differetiate the two ety type fields
    ticks_graph = range(0,120,10) if normalized else range(0,170,20)
    labels_graph = range(0,120,10) if normalized else range(0,170,20)
    
    # plt.yticks(ticks=range(0,100,10), labels=range(0,190,20)) #  labels=columns
    plt.yticks(ticks=ticks_graph, labels=labels_graph) #  labels=columns
    plt.title(f'{ety_version_title} Etymology Types by Decade{normalization_extension_title}')
    # plt.show()
    plt.savefig(f"figures/bar_graph_{ety_version_title}_ety_types_by_decade{normalization_extension_fig_name}.png", bbox_inches='tight')
    plt.clf()
    # the_table = plt.table(cellText=cell_text,
    #                       rowLabels=rows,
    #                       rowColours=colors,
    #                       colLabels=columns,
    #                       loc='bottom',
    #                       colWidths=(0.073,)*len(columns),
    #                     #   colWidths=[0.5 for i in n_rows],
    #                     colLoc='center'
    #                       )
    # plt.show()
    

key_to_long_title = {
   "PL": "Programming Languages",
   "CP": "Anaconda Packages",
   "RG": "Ruby Gems",
   "PM": "Package Managers",
   "ALL": "All Analyzed Software",
   "CH": "Cultural Heritage"
}

def get_bargraph_data(data_set, path):
    """
    Extracts the data of a specified .csv file (path), from a specific data set (set)
    """
    path = file_names[path]+data_set
    data = read_csv(path)
    return [data[0], [int(data[1][j]) for j in range(0, len(data[0]))] ]

def bar_graphs_morphemes(set):
    """
    Creates a bar graph for number of morphemes for a given data set. 
    """
    data = get_bargraph_data(set, "morpheme")
    # plt.rcParams['figure.figsize'] = [5, 7]
    plt.figure(figsize=(5,7))
    plt.xlabel("Number of Morphemes")
    plt.ylabel("Frequency")
    plt.title(f"Number of Morphemes for\n{key_to_long_title[set]}")
    plt.xticks([i for i in range(0, 5)])
    plt.bar(data[0][0:5], data[1][0:5], color ='navy')
    plt.savefig(f"figures/bar_graph_morphemes_{set}.png", bbox_inches='tight')
    plt.clf()
    
    return

def pls_top_for_morphemes():

    
    
    return 

def new_line_for_space(data):
    """
    TODO
    """
    for i in range(0, len(data[0])):
        while(True):
            if " " in data[0][i]:
                data[0][i] = data[0][i].replace(" ", "\n")
            else:
                break
    return data

def standardized_ety_types(filename):
    
    return

def get_mean_special(data):
    """
    Computes the mean of a given data set
    """
    morph_sum = 0
    for i in range(0, len(data[1])):
        morph_sum += (i+1) * data[1][i]
    return morph_sum/sum(data[1]) 

def get_variance_special(data, mean):
    """
    computes the variance of an array of numbers
    TODO: verify this
    """
    variance = 0
    for i in range(0, len(data[0])):
        variance += (((i+1)-mean))**2*data[1][i]
    return variance/sum(data[1])

def get_median_special(data):
    """
    Finds the median of an array of frequencies of numbers
    """
    median_threshold = np.ceil(sum(data[1])/2)
    running_sum = 0
    for i in range(0, len(data[0])):
        running_sum += data[1][i]
        if running_sum >= median_threshold:
            return data[0][i]
    raise Exception("Median could not be found. Programming error.")

def get_max_min(the_array):
    """
    gets the minimum and maximum values of an array
    """            
    return [np,min(the_array), np.max(the_array)]

def get_max_min_special(data):
    """
    Extracts the minimum and maximum values of a given array
    Assumption: 0 is the minimum value
    """
    minmax = [0, 0]

    # finding min
    for i in range(0, len(data[0])):
        if data[1][i] != 0:
            minmax[0] = data[0][i]
            break
    
    # finding max
    for i in range(len(data[0])-1, 0, -1):
        if data[1][i] != 0:
            minmax[1] = data[0][i]
            break
            
    return minmax[0], minmax[1]
        
def stats_on_numbers(set_name, path, array_data=[]):
    """
    Given a path to a file, generates a couple of basic
    statistical measures on the numbers present in that file
    """
    if len(array_data) != 0:
        exit()
    else:
        data = get_bargraph_data(set_name, path)

        mean = get_mean_special(data)
        median = get_median_special(data) # TODO: check if this is correct
        variance = get_variance_special(data, mean)
        std = np.around(math.sqrt(variance), 2) # irrelevant whether we do variance or std first
        min_max_values = get_max_min_special(data)

    print("Data Set & Mean & Median & Standard Deviation & Variance & Min Value & Max Value \\\\")
    return [
            set_name,
            np.round(mean, 2),
            int(median),
            '{:.2f}'.format(np.round(std, 2)),
            '{:.2f}'.format(np.round(variance, 2)),
            int(min_max_values[0]),
            int(min_max_values[1])
        ]


def bar_graphs_ch():
    """
    Generates a bar graph for the "Culutral Heritage" analysis
    """
    data = get_bargraph_data("", "CH")
    data = new_line_for_space(data)

    plt.xlabel("Categories of Cultural Heritage")
    plt.ylabel("Frequency")
    plt.title("Names with Cultural Heritage")
    plt.xticks(rotation=59)
    plt.subplots_adjust(bottom=0.3)
    plt.bar(data[0], data[1], color ='navy')
    plt.savefig(f"figures/bar_graph_cultural_heritage.png")
    plt.clf()
    
    return


def bar_graphs_characters(set):
    """
    Creates bar graphs for the number of characters of names,
    for a given data set
    """
    data = get_bargraph_data(set, "name_length")
    
    plt.figure(figsize=(10,3))
    plt.xlabel("Number of Characters")
    plt.ylabel("Frequency")
    plt.title(f"Character Length {key_to_long_title[set]}")
    plt.xticks([i for i in range(0, 35)])
    
    plt.bar(data[0], data[1], color ='navy')
    # plt.show()
    plt.savefig(f"figures/bar_graph_len_characters_{set}.png", bbox_inches='tight')
    plt.clf()
    return

def print_length_stats_latex(stat_dataa, set_names):
    """
    Allows for super fast intergration of a vector of statistical data into a Latex table
    """
    print("Data Set & Mean & Median & Standard Deviation & Variance & Min Value & Max Value \\\\")
    print("\hline")
    for i in range(0, len(stat_dataa)):
        the_string = f"{set_names[i]} & "
        for j in range(1, len(stat_dataa[0])):
            the_string += f"{stat_dataa[i][j]}  & "
        print(the_string[0:len(the_string)-3] + "\\\\\n\\hline") # space, ampersand, space
        
    return

def bar_graphs_characters_by_year():
    data = get_bargraph_data("PL", path)
    return

def version_numbering(data_set):
    
    return


    
    
def ety_types_table_pl(filename):
    """
    Creates a STD vs "Missing" category plot. This is mainly to
    show that the ety types are becoming more heterogenous over time.
    """
    data_csv = read_csv(filename)
    decades, data, categories = data_csv[0], np.array(data_csv[1:len(data_csv)-1], dtype=int), data_csv[-1]
    
    pos_missing = np.array([string == "Missing" for string in categories].index(True))
    sums_column = data.sum(axis=0)

    standardized_data = normalize_data(data)
    table_data = [[], []]
    
    for i in range(0, len(data[0])): 
        table_data[0].append(np.round(np.std(standardized_data[:,i]), 2))
        table_data[1].append(np.round(data[pos_missing][i]/sums_column[i] if sums_column[i] != 0 else 0, 2))
    
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=80)
    # blue is the standard deviation
    ax.plot(linify(decades), table_data[0], color='b')
    ax.set_ylabel('Standard Deviation')
    ax.legend(["Standard Deviation"], loc='upper left')
    
    # red is the standard deviation
    ax2 = ax.twinx() 
    ax2.set_ylabel("Percentage 'Missing'")
    ax2.plot(linify(decades), table_data[1], color='r')
    
    plt.legend(["Percentage 'Missing'"], loc='upper right')
    plt.title("Standard Deviation & Percentage 'Missing'")
    plt.savefig(f"figures/bar_graph_2nd_ety_types_pl_std_vs_percentage_missing.png", bbox_inches='tight')
    plt.clf()
    
    return

def ety_types_bar_graph():
    """
    Creates a normalized stacked bar graph that compares the ratios of
    ety types between different data sets. 
    """
    data_csv = read_csv('ety_types_by_data_set')
    data_set_names = data_csv[0]
    ety_types_list = data_csv[1]
    raw_data = np.array(data_csv[2:], dtype=float)
    plt.figure(figsize=(10,5))

    print(ety_types_list)
    print(raw_data)
    colors = plt.cm.tab20((4./3*np.arange(len(ety_types_list))).astype(int))[::-1]
    
    raw_data_normalized = normalize_data(raw_data.T).T

    for row in range(0,len(ety_types_list)):
        bottoms = [0]*len(data_set_names) if row == 0 else bottoms + raw_data_normalized[:,row-1]
        plt.bar(data_set_names, raw_data_normalized[:,row], color=colors[row],  bottom=bottoms, align='center')

    plt.subplots_adjust(right=0.7)
    plt.legend(ety_types_list, loc='center left', bbox_to_anchor=(1.2, 0.5))
    plt.title("2nd Ety. Types per Data Set")
    plt.xlabel("Data Sets")
    plt.ylabel("Relative Percentage of 2nd Ety. Types")
    plt.savefig(f"figures/bar_graph_2nd_ety_types_data_sets.png", bbox_inches='tight')

    return
# -------------------------------
# ------- VISUALIZATION ---------
# -------------------------------


# NUMBER OF CHARACTERS

# number of characters per set
# bar_graphs_characters("ALL")
# bar_graphs_characters("PL")
# bar_graphs_characters("CP")
# bar_graphs_characters("RG")
# bar_graphs_characters("PM")

# bar_graphs_characters_by_year()

# noc_all = stats_on_numbers("All", "name_length", "Number of Characters")
# noc_pl = stats_on_numbers("PL", "name_length", "Number of Characters")
# noc_cp = stats_on_numbers("CP", "name_length", "Number of Characters")
# noc_rg = stats_on_numbers("RG", "name_length", "Number of Characters")
# noc_pm = stats_on_numbers("PM", "name_length", "Number of Characters")


# NUMBER OF MORPHEMES

# number morphemes per set
# bar_graphs_morphemes("ALL")
# bar_graphs_morphemes("PL")
# bar_graphs_morphemes("CP")
# bar_graphs_morphemes("RG")
# bar_graphs_morphemes("PM")


# statistical data on mophemes per set
# nom_all = stats_on_numbers("All", "morpheme", "Number of Morphemes")
# nom_pl = stats_on_numbers("PL", "morpheme", "Number of Morphemes")
# nom_cp = stats_on_numbers("CP", "morpheme", "Number of Morphemes")
# nom_rg =  stats_on_numbers("RG", "morpheme", "Number of Morphemes")
# nom_pm = stats_on_numbers("PM", "morpheme", "Number of Morphemes")
# nom_top = stats_on_numbers("TOP", "morpheme", "Number of Morphemes")
# print_length_stats_latex([nom_all, nom_pl, nom_cp, nom_rg, nom_pm, nom_top], ["All", "PL", "CP", "RG", "PM", "TOP"])

# etymological depths
number_of_depths("ety_depths") # defaults to all
number_of_depths("ety_depths", "PL")
number_of_depths("ety_depths", "CP")
number_of_depths("ety_depths", "RG")
number_of_depths("ety_depths", "PM")

# ety types per decade
# ety_types('ety_type_1_by_decade')
# ety_types('ety_type_2_by_decade')

# stats on ety types
# ety_types_table_pl('ety_type_2_by_decade')
# ety_types_bar_graph()
# ety_types('ety_type_2_by_decade', normalized=True)
# ety_types_table_pl('ety_type_2_by_decade')

# cultural heritage
# bar_graphs_ch() # "CH", 'cultural_heritage'

# version numbering
# version_numbering("All")
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon')

from analysis.config import file_names, root
from analysis.file_management import read_csv


key_to_long_title = {
   "PL": "Programming Languages",
   "CP": "Anaconda Packages",
   "RG": "Ruby Gems",
   "PM": "Package Managers",
   "ALL": "All Analyzed Software",
   "CH": "Cultural Heritage"
}

def print_length_stats_latex(stat_dataa, set_names):
    """
    Allows for super fast intergration of a vector of statistical data into a
    Latex table
    """
    print("Data Set & Mean & Median & Standard Deviation & Variance & Min Value & Max Value \\\\")
    print("\hline")
    for i in range(0, len(stat_dataa)):
        the_string = f"{set_names[i]} & "
        for j in range(1, len(stat_dataa[0])):
            the_string += f"{stat_dataa[i][j]}  & "
        print(the_string[0:len(the_string)-3] + "\\\\\n\\hline") # space, ampersand, space
        
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

def linify(data):
    """
    Adds a line line for label headings so that they are easily readable
    """
    return [data[i].replace('-','-\n')for i in range(0, len(data))]


def convert_to_ints(data):
    """
    Converts an array of stringified integers to integers
    """
    for i in range(0,len(data)):
        for j in range(0,len(data[i])):
            data[i][j] = int(data[i][j])
    return np.array(data)
        
        
def get_bargraph_data(data_set, path):
    """
    Extracts the data of a specified .csv file (path), from a specific data set (set)
    """
    path = file_names[path] + data_set
    data = read_csv(path)
    return [data[0], [int(data[1][j]) for j in range(0, len(data[0]))] ]

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
    Creates a simple bar graphs, given the appropriate inputs. 'info' is a
    dictionary consisting of 'xlabel', 'ylabel' and 'title'. Skipping any of
    these parameters will cause an error
    """
    
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

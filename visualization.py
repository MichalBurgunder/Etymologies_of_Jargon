import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import sys  
import random      
sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon/analysis')


from analysis.file_management import read_csv
from analysis.config import file_names
# from analysis import config
# os.system('clear')


root = '/Users/michal/Documents/thesis/etymologies_of_jargon/results'


def create_bar_graph(ys, xs, info, log=False):
    fig = plt.figure()
    
    plt.xlabel(info["xlabel"])
    plt.ylabel(info["ylabel"])
    plt.title(info["title"])
    
    # the bar plot
    if not log:
        plt.bar(xs, ys, color ='navy',
            width = 0.4)
        plt.show()
        return
    
    # linear
    plt.subplot(221)
    plt.plot(xs, ys, color ='navy',)
    plt.yscale('linear')
    plt.title('linear')
    plt.grid(True)

    # log
    plt.subplot(222)
    plt.plot(xs, ys)
    plt.yscale('log')
    plt.title('log')
    plt.grid(True)
    plt.show()
    return
   
def depths(file_name):
    nums = read_csv(file_name, field=1)

    max_value = max(nums)

    bars = []
    for i in range(0, max_value+1+1): # +1 to add the last one, +1 to signify the end
        bars.append(nums.count(i))
    
    # now we simply pyplot
    # print(bars)
    info = {
        "xlabel": "Occurances",
        "ylabel": "No. of Etymology Depths",
        "title": "Number of Etymologies of Specific Depth"
    }
    return create_bar_graph(list(bars), list(range(0, len(bars))), info, True)

def convert_to_ints(data):
    for i in range(0,len(data)):
        for j in range(0,len(data[i])):
            data[i][j] = int(data[i][j])
    return np.array(data)
        
def order_data_by_frequency(data, old_rows):
    sorted_sums = sorted([(sum(data[i]), i) for i in range(0,len(data))])
    sorted_sums.reverse()
    
    sorted_data = []
    new_rows = []
    for i in range(0, len(data)):
        sorted_data.append(data[sorted_sums[i][1]])
        new_rows.append(old_rows[sorted_sums[i][1]])

    return sorted_data, new_rows
    
def ety_types(filename):
    data_csv = read_csv(filename)
    columns = data_csv[0] # fetching columns
    rows = data_csv[-1] # fetching rows
    data = data_csv[1:len(data_csv)-1]
    data = convert_to_ints(data)
    data, rows = order_data_by_frequency(data, rows)

    colors = plt.cm.tab20((4./3*np.arange(len(rows))).astype(int))

    n_rows = len(data)

    index = np.arange(len(columns))
    bar_width = 0.8

    # Initialize the vertical-offset for the stacked bar chart.
    # y_offset = np.ones(len(columns))
   

    fig, ax = plt.subplots(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    # Plot bars and create text labels for the table
    cell_text = []
    bottoms = None
    for row in range(0,n_rows):
        bottoms = [0]*len(columns) if row == 0 else bottoms + data[row-1]
        plt.bar(index, data[row], width=bar_width, bottom=bottoms, color=colors[row], align='center')
        cell_text.append(data[row])
        

    
    plt.xticks(ticks=[])
    # plt.yticks(ticks=range(0,35,6), labels=range(0,35,6)) #  labels=columns

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          loc='bottom',
                          colWidths=(0.073,)*len(columns),
                        #   colWidths=[0.5 for i in n_rows],
                        colLoc='center'
                          )
    # the_table.
    # fig, ax = plt.subplots(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    # [the_table.auto_set_font_size(False) for t in [tab1, tab2]]
    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.5)
   
    # plt.subplot(figsize=(16, 12))

    # plt.ylabel("Loss in ${0}'s".format(value_increment))
    # plt.yticks(values * value_increment, ['%d' % val for val in values])
    # plt.xticks([])
    plt.xticks(ticks=[])
    plt.yticks(ticks=range(0,190,20), labels=range(0,190,20)) #  labels=columns
    plt.title('Etymology Types by Decade')
    plt.show()

key_to_long_title = {
   "PL": "Programming Languages",
   "CP": "Anaconda Packages",
   "RG": "Ruby Gems",
   "PM": "Package Managers",
   "ALL": "All Analyzed Software",
}

short_to_file = {
   "PL": "Programming Languages",
   "CP": "Anaconda Packages",
   "RG": "Ruby Gems",
   "PM": "Package Managers"
}

def get_morpheme_data(set, show=False):
    data = read_csv(file_names["morpheme"]+set)
    return [[int(data[i][j]) for j in range(0, len(data[0]))] for i in range(0,2)]


def bar_graphs_morphemes(set):
    import matplotlib.pyplot as plt
    data = get_morpheme_data(set)
    plt.xlabel("Number of Morphemes")
    plt.ylabel("Frequency")
    plt.title(key_to_long_title[set])

    plt.bar(data[0], data[1], color ='navy')
    plt.savefig(f"figures/bar_graph_morphemes_{set}.png")
    plt.clf()
    return
# -------------------------------
# ------- VISUALIZATION ---------
# -------------------------------


# ety types per decade
# ety_types('ety_type_2_by_year')

# number morphemes per set
bar_graphs_morphemes("ALL")
bar_graphs_morphemes("PL")
bar_graphs_morphemes("CP")
bar_graphs_morphemes("RG")
bar_graphs_morphemes("PM")
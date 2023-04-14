import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import sys  
import random 
import os     
os.system('clear')
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

def linify(data):
    '''
    Adds a line line for label headings so that they are easily readable
    '''
    return [data[i].replace('-','-\n')for i in range(0, len(data))]

def normalize_data(data):
    '''
    Normalizes the data to a standard of 100, so that ety types can be compared over the decades
    '''
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
    
    # sums = np.array(data).sum(axis=0)
    # print(np.array(data))
    # exit()
    colors = plt.cm.tab20((4./3*np.arange(len(rows))).astype(int))

    n_rows = len(data)
    
    fig, ax = plt.subplots(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    
    # Plot bars and create text labels for the table
    cell_text = []
    bottoms = None
    for row in range(0,n_rows):
        bottoms = [0]*len(columns) if row == 0 else bottoms + data[row-1]
        # plt.bar(columns, data[row], width=bar_width, bottom=bottoms, color=colors[row], align='center')
        plt.bar(columns, data[row], color=colors[row],  bottom=bottoms, align='center')
        cell_text.append(data[row])
        

    
    # plt.xticks(ticks=[])
    # plt.yticks(ticks=range(0,35,6), labels=range(0,35,6)) #  labels=columns

    # Add a table at the bottom of the axes
    # the_table = plt.table(cellText=cell_text,
    #                       rowLabels=rows,
    #                       rowColours=colors,
    #                       colLabels=columns,
    #                       loc='bottom',
    #                       colWidths=(0.073,)*len(columns),
    #                     #   colWidths=[0.5 for i in n_rows],
    #                     colLoc='center'
    #                       )

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
    ticks_graph = range(0,120,10) if normalized else range(0,190,20)
    labels_graph = range(0,120,10) if normalized else range(0,190,20)
    
    # plt.yticks(ticks=range(0,100,10), labels=range(0,190,20)) #  labels=columns
    plt.yticks(ticks=ticks_graph, labels=labels_graph) #  labels=columns
    plt.title(f'Etymology Types by Decade{normalization_extension_title}')
    plt.show()
    plt.savefig(f"figures/bar_graph_2nd_ety_types_by_decade{normalization_extension_fig_name}.png")
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

def get_bargraph_data(set, path=False):
    path = file_names["morpheme"]+set if not path else path
    data = read_csv(path)
    return [data[0], [int(data[1][j]) for j in range(0, len(data[0]))] ]


def bar_graphs_morphemes(set):
    import matplotlib.pyplot as plt
    data = get_bargraph_data(set)
    plt.xlabel("Number of Morphemes")
    plt.ylabel("Frequency")
    plt.title(key_to_long_title[set])
    plt.xticks([i for i in range(0, 9)])
    plt.bar(data[0], data[1], color ='navy')
    plt.savefig(f"figures/bar_graph_morphemes_{set}.png")
    plt.clf()
    return

def new_line_for_space(data):
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
    morph_sum = 0
    for i in range(0, len(data[1])):
        morph_sum += (i+1) * data[1][i]
    return morph_sum/sum(data[1]) 

def get_variance_special(data, mean):
    variance = 0
    for i in range(0, len(data[0])):
        variance += (((i+1)-mean))**2*data[1][i]
    return variance/sum(data[1])

def stats_on_numbers(set):
    data = get_bargraph_data(set)
    
    mean = get_mean_special(data)
    variance = get_variance_special(data, mean)

    print(f"{set} Mean: {np.round(mean, 2)}")
    print(f"{set} Variance: {np.round(variance, 2)}")
    print()
    return [mean, variance]


def bar_graphs_ch():
    data = get_bargraph_data("CH", 'cultural_heritage')
    print(data)
    data = new_line_for_space(data)
    print(data)

    plt.xlabel("Number of Morphemes")
    plt.ylabel("Frequency")
    plt.title("Names with Cultural Heritage")
    
    plt.xticks(rotation=59)
    # plt.subplots_adjust(bottom=0.2)
    plt.subplots_adjust(bottom=0.3)
    plt.bar(data[0], data[1], color ='navy')
    # plt.show()
    plt.savefig(f"figures/bar_graph_cultural_heritage.png")
    plt.clf()
    return

def bar_graphs_character_length(set):
    import matplotlib.pyplot as plt
    data = get_bargraph_data(set)
    plt.xlabel("Number of Morphemes")
    plt.ylabel("Frequency")
    plt.title(key_to_long_title[set])
    plt.xticks([i for i in range(0, 9)])
    plt.bar(data[0], data[1], color ='navy')
    plt.savefig(f"figures/bar_graph_morphemes_{set}.png")
    plt.clf()
    return

def bar_graphs_characters(set):
    data = get_bargraph_data(set, "name_length")
    
    
    return 
# -------------------------------
# ------- VISUALIZATION ---------
# -------------------------------

# ety types per decade
# ety_types('ety_type_1_by_decade')
# ety_types('ety_type_2_by_decade')
# ety_types('ety_type_2_by_decade', normalized=True)

# number of characters per set
bar_graphs_characters('ALL')

# number morphemes per set
# bar_graphs_morphemes("ALL")
# bar_graphs_morphemes("PL")
# bar_graphs_morphemes("CP")
# bar_graphs_morphemes("RG")
# bar_graphs_morphemes("PM")

# statistical data on mophemes per set
stats_on_numbers("All")
stats_on_numbers("PL")
stats_on_numbers("CP")
stats_on_numbers("RG")
stats_on_numbers("PM")

# cultural heritage
# bar_graphs_ch() # "CH", 'cultural_heritage'

# ety types 2 frequencies
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import sys  
import random      
sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon/analysis')

import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap



from analysis.file_management import read_csv
# from analysis import config
# os.system('clear')


root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data'


def create_bar_graph(bars, log=False):
    xs = list(range(0, len(bars)))
    ys = list(bars)
    
    fig = plt.figure()
    
    plt.xlabel("Occurances")
    plt.ylabel("No. of Etymology Depths")
    plt.title("Number of Etymologies of Specific Depth")
    
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
    print(bars)
    return create_bar_graph(bars, True)

def convert_to_ints(data):
    for i in range(0,len(data)):
        for j in range(0,len(data[i])):
            data[i][j] = int(data[i][j])
    return np.array(data)
        
def order_data_by_frequency(data):
    sorted_sums = sorted([(sum(data[i]), i) for i in range(0,len(data))])
    sorted_sums.reverse()
    
    sorted_data = []
    for i in range(0, len(data)):
        sorted_data.append(data[sorted_sums[i][1]])

    return sorted_data
    
def ety_types(filename):
    data_csv = read_csv(filename)
    columns = data_csv[0] # fetching columns
    rows = data_csv[-1] # fetching rows
    data = data_csv[1:len(data_csv)-1]
    data = convert_to_ints(data)
    data = order_data_by_frequency(data)

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
    plt.yticks(ticks=range(0,30,5), labels=range(0,30,5)) #  labels=columns

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
    plt.yticks(ticks=range(0,30,5), labels=range(0,30,5)) #  labels=columns
    plt.title('Etymology Types by Decade')
    plt.show()

    
ety_types('ety_type_by_year')
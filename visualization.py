import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import sys        
sys.path.append('/Users/michal/Documents/thesis/etymologies_of_jargon/analysis')

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
    return data
            
def ety_types(filename):
    data = read_csv(filename)
    columns = data[0] # fetching columns
    rows = data[-1] # fetching rows
    data_stringed = data[1:len(data)-1] # clean data is left behind
    data = convert_to_ints(data_stringed)

    # Get some pastel shades for the colors
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
    colors = plt.cm.tab20(np.linspace(0, 0.5, len(rows)))

    n_rows = len(data)

    index = np.arange(len(columns))
    bar_width = 0.8

    # Initialize the vertical-offset for the stacked bar chart.
    # y_offset = np.ones(len(columns))

    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(0,n_rows):
        # print(data[row])
        plt.bar(index, data[row], width=bar_width, color=colors[row], align='center')
        cell_text.append(data[row])
    # Reverse colors and text labels to display the last value at the top.
    colors = colors[::-1]
    plt.xticks(ticks=[])
    plt.yticks(ticks=range(0,30,5), labels=range(0,30,5)) #  labels=columns
    # plt.show()
    # exit()
    # cell_text.reverse()
    # print(colors)
    # print(len(colors))
    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          loc='bottom',
                          colWidths=(0.072,)*len(columns),
                        #   colWidths=[0.5 for i in n_rows],
                        colLoc='center'
                          )
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
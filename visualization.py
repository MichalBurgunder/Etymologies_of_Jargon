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
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    # with open(f"{root}/final_data/{file_name}.csv", ) as file:
    #     info = csv.reader(file, delimiter=',')
    #     next(info) # skip the header
    #     for row in info:
    #         nums.append(int(row[1]))

    max_value = max(nums)

    bars = []
    for i in range(0, max_value+1+1): # +1 to add the last one, +1 to signify the end
        bars.append(nums.count(i))
    
    # now we simply pyplot
    print(bars)
    return create_bar_graph(bars, True)

def ety_types(filename):
    data = read_csv(filename)

    # columns = ('Freeze', 'Wind', 'Flood', 'Quake', 'Hail')
    columns = data[0]
    # rows = ['%d year' % x for x in (100, 50, 20, 10, 5)]
    rows = data[-1]
    data = data[1:len(data)-1]
    # print(data)
    # print(len(data))
    # exit()
    # values = np.arange(0, 2500, 500)
    # value_increment = 1000

    # Get some pastel shades for the colors
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
    n_rows = len(data)
    # print(data)
    # exit()
    index = np.arange(len(columns)) + 0.3
    bar_width = 0.4

    # Initialize the vertical-offset for the stacked bar chart.
    y_offset = np.zeros(len(columns))

    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(0,n_rows):
        plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
        print(data[row])
        print(y_offset)
        # y_offset = y_offset + data[row]
        cell_text.append(['%1.1f' % (x / 1000.0) for x in y_offset])
    # Reverse colors and text labels to display the last value at the top.
    colors = colors[::-1]
    cell_text.reverse()

    # Add a table at the bottom of the axes
    print(columns)
    print(len(columns))
    print(rows)
    print(len(rows))
    # exit()
    the_table = plt.table(cellText=cell_text,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          loc='bottom')

    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.2)

    # plt.ylabel("Loss in ${0}'s".format(value_increment))
    # plt.yticks(values * value_increment, ['%d' % val for val in values])
    # plt.xticks([])
    plt.title('Loss by Disaster')

    plt.show()
    
ety_types('ety_type_by_year')
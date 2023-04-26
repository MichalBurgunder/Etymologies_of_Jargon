import numpy as np
import matplotlib.pyplot as plt

from visualization_utils import convert_to_ints, read_csv, linify, root

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
    plt.savefig(f"{root}/figures/bar_graph_{ety_version_title}_ety_types_by_decade{normalization_extension_fig_name}.png", bbox_inches='tight')
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
    plt.savefig(f"{root}/figures/bar_graph_2nd_ety_types_pl_std_vs_percentage_missing.png", bbox_inches='tight')
    plt.clf()
    
    return



def ety_types_bar_graph_normalized():
    """
    Creates a normalized stacked bar graph that compares the ratios of
    ety types between different data sets. 
    """
    data_csv = read_csv('ety_types_by_data_set')
    data_set_names = data_csv[0]
    ety_types_list = data_csv[1]
    raw_data = np.array(data_csv[2:], dtype=float)
    plt.figure(figsize=(10,5))

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
    plt.savefig(f"{root}/figures/bar_graph_2nd_ety_types_data_sets.png", bbox_inches='tight')

    return


import matplotlib.pyplot as plt

from visualization_utils import get_bargraph_data, key_to_long_title
from visualization_utils import root

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

    plt.savefig(f"{root}/figures/bar_graph_morphemes_{set}.png", bbox_inches='tight')
    plt.clf()
    
    return

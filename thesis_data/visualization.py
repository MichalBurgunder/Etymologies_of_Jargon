
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

os.system('clear')

root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data'


def create_bar_graph(bars):
    xs = list(range(0, len(bars)))
    ys = list(bars)
    
    fig = plt.figure()
    
    # the bar plot
    plt.bar(xs, ys, color ='navy',
            width = 0.4)
    
    plt.xlabel("Occurances")
    plt.ylabel("No. of Etymology Depths")
    plt.title("Number of Etymologies of Specific Depth")
    plt.show()
    
    
def depths():
    nums = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/final_data/ety_depths.csv", ) as file:
        info = csv.reader(file, delimiter=',')
        next(info) # skip the header
        for row in info:
            nums.append(int(row[1]))

    # now we simply pyplot
    max_value = max(nums)
    bars = []
    for i in range(1, max_value):
        bars.append(nums.count(i))
    
    return create_bar_graph(bars)
    
depths()
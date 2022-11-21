
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

os.system('clear')

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


    
    
    
def depths():
    nums = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/final_data/ety_depths.csv", ) as file:
        info = csv.reader(file, delimiter=',')
        next(info) # skip the header
        for row in info:
            nums.append(int(row[1]))
            if row[0] == "J#":
                print("here")
                print(row)
                # exit()


    max_value = max(nums)
    # print(max_value)
    # exit()
    bars = []
    for i in range(0, max_value+1+1): # +1 to add the last one, +1 to signify the end
        bars.append(nums.count(i))
    
    # now we simply pyplot
    print(bars)
    return create_bar_graph(bars, True)
    
depths()

import numpy as np
import math

from visualization_utils import get_bargraph_data

def stats_on_numbers(set_name, path, array_data=[]):
    """
    Given a path to a file, generates a couple of basic
    statistical measures on the numbers present in that file
    """
    if len(array_data) != 0:
        exit()
    else:
        data = get_bargraph_data(set_name, path)

        mean = get_mean_special(data)
        median = get_median_special(data) # TODO: check if this is correct
        variance = get_variance_special(data, mean)
        std = np.around(math.sqrt(variance), 2) # irrelevant whether we do variance or std first
        min_max_values = get_max_min_special(data)

    print("Data Set & Mean & Median & Standard Deviation & Variance & Min Value & Max Value \\\\")
    return [
            set_name,
            np.round(mean, 2),
            int(median),
            '{:.2f}'.format(np.round(std, 2)),
            '{:.2f}'.format(np.round(variance, 2)),
            int(min_max_values[0]),
            int(min_max_values[1])
        ]
    
def get_mean_special(data):
    """
    Computes the mean of a given data set
    """
    morph_sum = 0
    for i in range(0, len(data[1])):
        morph_sum += (i+1) * data[1][i]
    return morph_sum/sum(data[1]) 

def get_variance_special(data, mean):
    """
    computes the variance of an array of numbers
    TODO: verify this
    """
    variance = 0
    for i in range(0, len(data[0])):
        variance += (((i+1)-mean))**2*data[1][i]
    return variance/sum(data[1])

def get_median_special(data):
    """
    Finds the median of an array of frequencies of numbers
    """
    median_threshold = np.ceil(sum(data[1])/2)
    running_sum = 0
    for i in range(0, len(data[0])):
        running_sum += data[1][i]
        if running_sum >= median_threshold:
            return data[0][i]
    raise Exception("Median could not be found. Programming error.")

def get_max_min(the_array):
    """
    gets the minimum and maximum values of an array
    """            
    return [np,min(the_array), np.max(the_array)]

def get_max_min_special(data):
    """
    Extracts the minimum and maximum values of a given array
    Assumption: 0 is the minimum value
    """
    minmax = [0, 0]

    # finding min
    for i in range(0, len(data[0])):
        if data[1][i] != 0:
            minmax[0] = data[0][i]
            break
    
    # finding max
    for i in range(len(data[0])-1, 0, -1):
        if data[1][i] != 0:
            minmax[1] = data[0][i]
            break
            
    return minmax[0], minmax[1]

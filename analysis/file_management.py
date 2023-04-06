
import csv
from os.path import exists
import random

from config import raw_data_root, root

global options 
global run_options 


def write_into_one_csv(root, paths, descriptor, just_headers=False):
    """
    Because having multiple CSV files is irrelevant to the anaylysis,
    we combine all inputted CSV files and combine them into one. This 
    data is then saved into a "{root}/temp_{descriptor}.csv".
    """
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/temp_{descriptor}.csv", "wt") as fw:
        writer = csv.writer(fw)
        for path in paths:
            if not exists(f"{raw_data_root}/{path}"):
                print(f"Cannot find path to file {raw_data_root}/{path}.")
                print("Missing a comma, maybe?")
                print("Exiting...")
                exit()
            with open(f"{raw_data_root}/{path}", ) as file:
                info = csv.reader(file, delimiter=',')
                if not just_headers:
                    next(info) # skip the header
                for row in info:
                    writer.writerow(row)
                    if just_headers:
                        break
    return f"{root}/temp_{descriptor}.csv"

# format data --> place then arrays, to work with csvs
def save_as_csv(data, descriptor, format_data=False, options={}):
    """
    Saves all the data into a CSV.
    """
    if format_data:
        data = [[entry] for entry in data]
    subfolder = "results" if "subfolder" not in options else options["subfolder"]
    with open(f"{root}/{subfolder}/{descriptor}.csv", "wt") as fw:
        writer = csv.writer(fw)
        for row in data:
            writer.writerow(row)
    if 'v' in options and options['v']:
        print(f"new data written to {root}/temp_{descriptor}.csv")
    
def save_as_txt(root, data, descriptor, final=False):
    """
    Saves all the data into a text file.
    """
    d = "final" if final else "temp"
    with open(f"{root}/{d}_{descriptor}.txt", "wt") as fw:
        writer = csv.writer(fw)
        writer.writerow(data)

def read_csv(file_name, field=False, sub_directory='final_data/'):
    """
    Reads out of a CSV and inserts all of the lines in it into an array.
    """
    lines = []
    with open(f"{root}/{sub_directory}{file_name}.csv") as file:
        info = csv.reader(file, delimiter=',')
        for row in info:
            if field != False:
                lines.append(row[field])
            else: 
                 lines.append(row)

    return lines



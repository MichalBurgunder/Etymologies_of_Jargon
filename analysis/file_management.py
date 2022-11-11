
import csv
from os.path import exists

def write_into_one_csv(root, paths, descriptor, just_headers=False):
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/temp_{descriptor}", "wt") as fw:
        writer = csv.writer(fw)
        for path in paths:
            if not exists(f"{root}/{path}"):
                print(f"Cannot find path to file {root}/{path}. Exiting...")
            with open(f"{root}/{path}", ) as file:
                info = csv.reader(file, delimiter=',')
                if not just_headers:
                    next(info) # in an attempt to skip the header
                for row in info:
                    writer.writerow(row)
                    if just_headers:
                        break
    return f"{root}/temp_{descriptor}"

def save_as_csv(root, data, descriptor, headers, final=False, format_data=False, ):
    if format_data:
        new_data = []
        for entry in data:
            new_data.append([entry])
        data = new_data
        
    with open(f"{root}/temp_{descriptor}.csv", "wt") as fw:
        writer = csv.writer(fw)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
    print(f"new data written to {root}/temp_{descriptor}.csv")
    
def save_as_txt(root, data, descriptor, final=False):
    d = "final" if final else "temp"
    with open(f"{root}/{d}_{descriptor}.txt", "wt") as fw:
        writer = csv.writer(fw)
        writer.writerow(data)

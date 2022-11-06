
import csv

def write_into_one_csv(root, paths, descriptor, just_headers=False):
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    with open(f"{root}/temp_{descriptor}", "wt") as fw:
        writer = csv.writer(fw)
        for path in paths:
            with open(f"{root}/{path}", ) as file:
                info = csv.reader(file, delimiter=',')
                if not just_headers:
                    next(info) # in an attempt to skip the header
                for row in info:
                    writer.writerow(row)
                    if just_headers:
                        break
    return f"{root}/temp_{descriptor}"

def save_as_csv(root, data, descriptor, headers):
    with open(f"{root}/temp_{descriptor}.csv", "wt") as fw:
        writer = csv.writer(fw)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

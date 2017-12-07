import csv

def csv_load(filename):
    list_data = []

    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            list_data.append(row)

    return list_data

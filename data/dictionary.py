import csv

def dict_to_csv(csv_file,dictionary):
    writer = csv.writer(csv_file)
    for key, value in dictionary.items():
        writer.writerow([key, value])

def csv_to_dict(csv_file):
    reader = csv.reader(csv_file)
    return dict(reader)
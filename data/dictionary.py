import csv

def dict_to_csv(csv_file,dictionary):
    writer = csv.writer(csv_file)
    for key, value in dictionary.items():
        writer.writerow([key, value])

def csv_to_dict(csv_file):
    reader = csv.reader(csv_file)
    return dict(reader)


class JSON_Parser():
    def __init__(self, json: dict):
        self.json = json

    def show_keys(self):
        self.recurse_keys(self.json, "")

    def recurse_keys(self, dictionary, indent):
        add_indent = "  "
        if type(dictionary) == dict:
            for key in list(dictionary.keys()):
                print(indent + str(key))
                self.recurse_keys(dictionary[key], indent + add_indent)

        # If you get a list which has dictionaries in it, recurse
        elif type(dictionary) == list:
            if len(dictionary) > 0 and type(dictionary[0]) == dict:
                for value in dictionary:
                    self.recurse_keys(value, indent + add_indent)
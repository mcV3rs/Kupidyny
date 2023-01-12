import csv

with open("project/instance/Karolina_Michał_wedding.csv", 'r') as f:
    dict_reader = csv.DictReader(f)

    list_of_dict = list(dict_reader)

    print(list_of_dict[0]["wife"])

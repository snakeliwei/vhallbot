import csv

filename = './user.csv'
with open(filename) as f:
    data = csv.DictReader(f)
    print(data)
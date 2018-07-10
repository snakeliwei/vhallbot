
from config import huey
from task import addjob
import csv


if __name__ == '__main__':
    url = 'http://live.vhall.com/914762818'
    filename = './user.csv'
    data = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    try:
        addjob(url, data)
    except Exception as err:
        print(err)

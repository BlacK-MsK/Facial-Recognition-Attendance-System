import csv
import datetime
import time
import os


def assure_path_exists(path, date):
    dir = os.path.dirname(path)
    dir = os.path.join(dir, date)
    if not os.path.exists(dir) :
        filename = "Attendance CSV/Attendance {}.csv".format(date)
        # writing to csv file
        with open(filename, 'w', newline='') as csvfile :
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(fields)
        print("CSV made")


fields = ['UID', 'Time', 'Date', 'Attendance']
path = "Attendance CSV/"

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

assure_path_exists(path, date)

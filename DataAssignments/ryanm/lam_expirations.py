import csv
import datetime


with open(r"C:\Users\ryanm\Desktop\Main\Analyses\2015\LAM Score\2015_03_03_Splunk_Fixed.csv", 'rb') as R:
    reader = csv.reader(R, delimiter=',')

    header = reader.next()

    for row in reader:
        sfid = row[header.index("SalesForceID")]

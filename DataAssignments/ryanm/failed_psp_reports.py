import LogFileTools.log_iterator as lf
import os
import csv
import datetime


log_files = "\\\\filer01\\public\\Data Dashboards\\PSP Reports\\"
log_files_to_use = []

countries = ['Canada', 'United States', 'United Kingdom']


for files in os.listdir(log_files):

    if "2014.09" in files:
        log_files_to_use.append(files)


for files in log_files_to_use:

    monthly_count = 0
    monthly_total_count = 0

    with open(log_files + files, 'rb') as R:
        reader = csv.reader(R, delimiter=',')

        header = reader.next()

        for row in reader:
            monthly_total_count += 1

            annualized = row[header.index('Annualized50')]

            if annualized == "":
                monthly_count += 1

    print "Failed Reports for " + files[:7] + " : " + str(monthly_count)
    print "Total Reports for " + files[:7] + " : " + str(monthly_total_count)

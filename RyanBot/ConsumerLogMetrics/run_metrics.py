import os
import time
import log_data
import dash_data


def web_traffic_reminder():

    path = '\\\\filer01\\public\\Data_Analytics\\'

    check = True

    mtime = time.ctime(os.path.getmtime(path + 'Web Traffic.csv'))

    good = ['', ' ']

    while check is True:

        print "The last time the Web Traffic.csv file at " + '\\\\pssea\\files\\public\\Data Analytics\\' + \
              ' was updated was ' + mtime + '. \n'

        answer = raw_input("If you want to update this file before moving forward do so now. When finished or \
                            if it's already updated press enter. \n")

        if answer in good:
            check = False

        elif answer not in good:
            print "Press enter to continue on with the program. Do not add any other input. \n"

web_traffic_reminder()

log_files_to_use = log_data.NewLogFiles().log_files_to_use

#Confirm job check
job_set = dash_data.DashReader().job_set

log_data.LogDataPull(log_files_to_use, job_set)
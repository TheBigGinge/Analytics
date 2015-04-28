import LogFileTools.log_iterator as log_tool
import datetime
import os
import csv


class CountPSPAccounts:

    def __init__(self, job_title_list):
        self.job_title_list = job_title_list
        self.accounts = set()
        self.reports = 0

    def pull_account_data(self):

        psp_path = "\\\\filer01\\public\\Data Dashboards\\PSP Reports\\"
        files_to_use = []

        for files in os.listdir(psp_path):
            if '2014' in files or '2013.12' in files or '2013.11' in files or '2013.10' in files:
                files_to_use.append(files)

        for files in files_to_use:
            print "Working on " + files
            with open(psp_path + files, 'rb') as R:
                reader = csv.reader(R, delimiter=',')

                header = reader.next()

                for row in reader:

                    id = row[header.index('SalesForce Acct ID')]
                    job = row[header.index('Job')]

                    if job == self.job_title_list:
                        self.accounts.add(id)
                        self.reports += 1

        print "Total accounts: " + str(len(self.accounts))
        print "Total reports: " + str(self.reports)

        with open("c:\\users\\ryanm\\desktop\\PSP Accounts.csv", 'wb') as W:
            writer = csv.writer(W, delimiter=',')

            for item in self.accounts:
                final = item, ""
                writer.writerow(final)


CountPSPAccounts("Registered Hospice Nurse (RN)").pull_account_data()
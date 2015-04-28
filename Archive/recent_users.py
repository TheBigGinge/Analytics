import datetime
import os
import csv

report_path = '\\\\pssea\\files\\public\\Data Dashboards\\PSP Reports\\'
metric_path = '\\\\pssea\\files\\public\\Data Analytics\\PSP Log Metrics\\Data Files\\'


class PSPReportCompile:

    def __init__(self):
        self.subscription_dict = {}
        self.pull_files_command()
        #self.create_new_mapping()

    @staticmethod
    def file_name():

        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month)

        if len(month) == 1:
            month = "0" + month

        final_date = year + '.' + month + ".csv"

        print final_date
        return final_date

    @staticmethod
    def file_name_alt():

        now = datetime.datetime.now()

        previous_month = now.month - 1

        if previous_month == 0:
            previous_year = now.year - 1
            previous_month = "12"
        else:
            previous_year = now.year
            previous_month = str(previous_month)

        if len(previous_month) == 1:
            previous_month = "0" + previous_month

        final_date = str(previous_year) + '.' + str(previous_month) + '.csv'

        return final_date

    def pull_files_command(self):

        try:
            self.file_pull(self.file_name())

        except IOError:
            print "Current PSP report doesn't exist yet. Pulling last months report " + self.file_name_alt()

            self.file_pull(self.file_name_alt())

        except WindowsError:
            print "Somebody has the file Account_ID_Lookup.csv open."
            raw_input("Once this file is closed press enter \n")

            self.file_pull(self.file_name())

    def file_pull(self, file_name):

        with open(os.path.join(report_path, file_name)) as f:
            reader = csv.reader(f, delimiter=',')
            names = reader.next()

            print "Compiling the users from the last month of PSP reports from the file " +\
                file_name + " \n"

            counter = 0

            for row in reader:
                counter += 1

                if counter % 10000 == 0:
                    print "Cycled through %s rows..." % counter

                account_id = row[names.index('Acct ID')]
                subscription_type = row[names.index('SubscriptionType')]

                if subscription_type in ['PSPV2 AD-HOC', 'PSPV2 MR T']:
                    final_subscription = "Market Rate"
                else:
                    final_subscription = 'Insight'

                self.subscription_dict[account_id] = final_subscription

    def create_new_mapping(self):

        file_name = 'Account_ID_Lookup.csv'

        current_mapping = {}

        with open(metric_path + file_name, 'rb') as R:
            reader = csv.reader(R, delimiter=',')

            names = reader.next()

            for row in reader:
                account_id = row[names.index('PSAccountID')]
                subscription = row[names.index('Subscription Type')]

                current_mapping[account_id] = subscription

        for keys in self.subscription_dict:
            current_mapping[keys] = self.subscription_dict[keys]

        with open(metric_path + file_name, 'w') as W:
            writer = csv.writer(W, lineterminator='\n')

            header = ['PSAccountID', 'Subscription Type']
            writer.writerow(header)

            for line in current_mapping:
                final = line, current_mapping[line]
                writer.writerow(final)

PSPReportCompile()
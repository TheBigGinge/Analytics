import os
import os.path
import csv
import getpass
import zipfile

import DateFunctions.date_functions as dates

#import recent_users


class PSPMetrics:

    def __init__(self):
        self.is_customer_data = []
        self.is_internal_data = []
        self.is_customer_dates = []
        self.is_internal_dates = []
        self.archived_zip_list = []
        self.working_directory = os.getcwd()
        self.local_path = os.path.expanduser("~"+getpass.getuser())+"\\desktop\\"
        self.data_path = '\\\\filer01\\public\\Data_Analytics\\PSP Log Metrics\\Data Files\\'
        self.zip_path = '\\\\filer01\\prodlogs\\Zips\\'
        self.i_web_01a = '\\\\insightweb01a\\LogFiles\\VerboseLog\\'
        self.i_web_01b = '\\\\insightweb01b\\LogFiles\\VerboseLog\\'
        self.i_web_02a = '\\\\insightweb03a\\LogFiles\\VerboseLog\\'
        self.i_web_02b = '\\\\insightweb03b\\LogFiles\\VerboseLog\\'
        self.account_dict = self.create_account_type_dictionary()

    def find_job_matching_files(self):

        for files in os.listdir(self.zip_path):
            if 'INSIGHTWEB03A' in files and 'VerboseLog' in files:
                self.archived_zip_list.append(files)
            elif 'INSIGHTWEB01A' in files and 'VerboseLog' in files:
                self.archived_zip_list.append(files)
            elif 'INSIGHTWEB02A' in files and 'VerboseLog' in files:
                self.archived_zip_list.append(files)
            elif 'INSIGHTWEB02B' in files and 'VerboseLog' in files:
                self.archived_zip_list.append(files)
            elif 'INSIGHTWEB03B' in files and 'VerboseLog' in files:
                self.archived_zip_list.append(files)
            elif 'INSIGHTWEB01B' in files and 'VerboseLog' in files:
                self.archived_zip_list.append(files)
            else:
                continue

    def create_account_type_dictionary(self):

        lookup_dict = {}

        with open(self.data_path + 'Account_ID_Lookup.csv', 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            names = reader.next()

            for row in reader:
                account_id = row[names.index('PSAccountID')]
                subscription = row[names.index('Subscription Type')]
                lookup_dict[account_id] = subscription

        return lookup_dict

    def cycle_zip_files(self):

        for i in range(0, len(self.archived_zip_list) - 1):
            try:
                self.zip_file_read(self.archived_zip_list[i])
            except KeyError:
                continue

    def zip_file_read(self, zip_file):

        full_zip_file = zipfile.ZipFile(self.zip_path + zip_file)
        file_list = full_zip_file.namelist()

        [self.extract_data(full_zip_file, file_name) for file_name in file_list if 'JobTitleMatchingV2' in file_name]
        try:
            [os.remove(self.working_directory + "\\" + file_name) for file_name in file_list
             if 'JobTitleMatchingV2' in file_name]
        except WindowsError:
            pass

    def extract_data(self, full_zip_file, file_name):

        current_year_month = dates.DateFunctions().return_year_month_as_string("")

        if current_year_month in file_name:
            pass
        else:
            full_zip_file.extract(file_name, self.working_directory)
            print "Working on " + file_name

            with open(self.working_directory + "\\" + file_name) as reader:
                for row in csv.reader(reader, delimiter=',', quotechar='"'):
                    #Get rid of bad rows
                    if len(row) < 16:
                        continue
                    else:
                        date = file_name[len('JobTitleMatchingV2_'):len('JobTitleMatchingV2_')+10]
                        mon, day, year = date[4:6], date[6:8], date[0:4]
                        final_date = year + '-' + mon

                        data = self.data_pull(row)
                        if data[6] is False:
                            self.is_internal_data.append(data)
                            self.is_internal_dates.append(final_date)
                        else:
                            self.is_customer_data.append(data)
                            self.is_customer_dates.append(final_date)

    def data_pull(self, csv_row):

        create_date = self.create_date(self.find_time(csv_row))
        position, query_count = self.find_position_and_query_count(csv_row)
        more_count = self.find_more_count(csv_row)
        number_searches = self.search_term_grab(csv_row)
        subscription_type = self.get_subscription_type(csv_row)
        is_customer = self.determine_user_type(csv_row)

        return create_date, position, query_count, more_count, number_searches, subscription_type, is_customer

    @staticmethod
    def determine_user_type(csv_row):
        final = None

        for item in csv_row:
            if "IsCustomer" in item:
                final = True
                break
            else:
                final = False

        return final

    @staticmethod
    def find_time(csv_row):
        time = csv_row[3]
        return time

        #The below code checks for all items that would need to there for it to be a time stamp in the log
        #Logs are more stable these days so I'm switching it over to just csv_row[3]
        #for item in csv_row:
        #    if '/' in item and item.find('/') != item.rfind('/') and '0' in item and ":" in item and '-' not in item \
        #            and item.isalpha() is False and len(item) == 24:
        #        return item
        #    else:
        #        return

    @staticmethod
    def create_date(find_time):
        mon, day, year = find_time[0:2], find_time[3:4], find_time[6:10]
        return year + '-' + mon

    @staticmethod
    def find_position_and_query_count(csv_row):
        position = None
        query_count = None

        for item in range(0, len(csv_row) - 1):
            try:
                if isinstance(int(csv_row[item]), int) is True and isinstance(int(csv_row[item+1]), int) is True:
                    position = csv_row[item]
                    query_count = csv_row[item + 1]

            except ValueError:
                continue

        return position, query_count

    @staticmethod
    def find_more_count(csv_row):

        more_count = None
        for item in range(0, len(csv_row)-1):
            if csv_row[item] == 'Search Result' or csv_row[item] == 'Pin title':
                more_count = csv_row[item + 1]
            elif csv_row[item] == 'default':
                more_count = csv_row[item-1]

        return more_count

    @staticmethod
    def search_term_grab(csv_row):

        for i, item in enumerate(csv_row):
            if 'jobmatch-incremental' in item:
                searches = csv_row[i+1].split(',')
                number_searches = len(searches)

                return number_searches

    def get_subscription_type(self, csv_row):

        account_id = None

        for i, item in enumerate(csv_row):
            if item == 'Information':
                try:
                    account_id = csv_row[i+1]
                except IndexError:
                    account_id = None
        try:
            subs_type = self.account_dict[account_id]
        except KeyError:
            subs_type = None

        return subs_type
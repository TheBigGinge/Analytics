import sys
sys.path.append("C:\\hg\\payscale\\users\\ryanm\\PayScaleAnalytics\\")
import RequestService.splunk_requests as splunk
import DateFunctions.datetimes_in as df
import csv


class SplunkDataToLogs:

    def __init__(self):
        self.min_date = None
        self.max_date = None
        self.file_path = '\\\\filer01\\public\\Data_Analytics\\Splunk_PSP_Metrics\\Data\\'
        self.header = ['AccountID', 'AccountName', 'Algorithm', 'Search Terms', 'Created', 'Email', 'Find Position',
                       'Query Count', 'More Count', 'PayscaleTitle', 'Queries', 'SalesForceAccountID',
                       'SubscriptionType']
        self.dates = df.DateTimeFormats()
        self.create_dates()

    def create_dates(self):
        self.min_date = self.dates.find_first_of_last_month()
        self.max_date = self.dates.find_first_of_current_month()

    def pull_splunk_data(self):

        return splunk.SplunkRequests(self.min_date, self.max_date).pull_psp_job_match_splunk_logs()

    def write_data_to_logs(self):
        splunk_data = self.pull_splunk_data()

        print "Writing %s to file..." % str(self.dates.return_today_as_y_m(""))

        with open(self.file_path + str(self.dates.return_today_as_y_m("")) + " Splunk_PSP_Logs.csv", 'w') as W:
            writer = csv.writer(W, lineterminator='\n')

            writer.writerow(self.header)

            for dictionary in splunk_data:
                row = []

                for i, item in enumerate(dictionary):
                    if i == 3:
                        query_count = self.count_query_string(dictionary[item])
                        row.append(query_count)
                    elif i == 4:
                        try:
                            new_date = self.date_strip(dictionary[item])
                        except IndexError:
                            new_date = str(self.dates.return_last_month_as_y_m("-"))

                        row.append(new_date)

                    else:
                        row.append(dictionary[item])

                row_length = len(row)

                if row_length == 13:
                    row_test = self.test_for_int(row)
                    if row_test is True:
                        writer.writerow(row)

    def current_date_check(self, date):

        if str(date) == str(self.max_date.strftime("%Y-%m")):
            return False
        else:
            return True

    @staticmethod
    def count_query_string(query_string):
        query_list = query_string.split(",")
        query_length = len(query_list)
        return str(query_length)

    def date_strip(self, date):
        items = str(date).split("/")
        year = items[2]
        year = year[:year.find(" ")]
        month = items[0]
        if len(month) == 1:
            month = "0" + month

        return year + '-' + month

    @staticmethod
    def test_for_int(character_list):

        for i, item in enumerate(character_list):
            if 6 <= i <= 8:
                try:
                    int(item)
                except ValueError:
                    return False
        return True

    def set_header(self, new_header):
        self.header = new_header

    def set_file_path(self, new_file_path):
        self.file_path = new_file_path


SplunkDataToLogs().write_data_to_logs()
import csv
import datetime
import time


class CSVLogIterator:

    def __init__(self, min_date,
                 max_date,
                 field_list=None,
                 values_to_find=None,
                 path_to_use='\\\\psfiler01\\data\\SurveyReports\\'):
        """
        :param min_date:
            datetime value of the start date of files you want to use
        :param max_date:
            datetime value of the end date of files you want to use
        :param field_list:
            not currently used
        :param values_to_find:
            not currently used

        Lots of data analysis here at Payscale requires going through the consumer logs on
        psfiler02. Instead of writing code over and over again you can use this class to get the
        files you're looking for.

        example:
            logger = CSVLogIterator(datetime.datetime(2014, 1, 1), datetime.datetime(2014, 3, 1))
            logger.find_all_logs_survey()


        """

        self.log_files_to_use = []
        self.new_file = False
        self.current_file = None
        self.path_to_use = path_to_use
        self.min_date = min_date
        self.max_date = max_date
        self.field_list = field_list
        self.header = None
        self.values_to_find = values_to_find
        self.storage_dict = {}
        self.file_name = []

    def iterate_files_return_row(self, signal=None):

        """Grabs the rows for you and lets you do all the dirty work"""

        for files in self.log_files_to_use:

            print 'Working on ' + files
            if signal is not None:
                pass
            try:
                csv_rows = self.open_file(files)
                self.new_file = False
                for row in csv_rows:
                    yield row

            except IOError:
                print "Missing the file " + files
                continue

    def iterate_files_return_dictionary(self):

        """Grab the values you want and return their counts as a dictionary"""

        for files in self.log_files_to_use:

            csv_rows = self.open_file(files)

            for row in csv_rows:

                [self.store_data_to_count_dictionary(row[self.header.index(value)], value) for value in row]

    def open_file(self, file_in):
        """Open the file as read binary but before that erase the header column so it can be refreshed"""
        self.new_file = True
        with open(self.path_to_use + file_in, 'rb') as R:

            reader = csv.reader(R, delimiter=',')

            self.header = reader.next()

            for row in reader:
                yield row

    def store_data_to_count_dictionary(self, value, name):

        try:
            self.storage_dict[name][value] += 1

        except KeyError:
            self.storage_dict[name] = {}
            self.storage_dict[name][value] = 1

    def find_all_logs_survey(self):
        """Use datetime to find all values between the min and max date,
        change those datetime's to strings, and append to the log_files_to_use_list
        This works for year, month, day dates like the logfile in survey profile data"""

        delta = self.max_date - self.min_date

        [self.log_files_to_use.append(self.datetime_to_logfile_string(self.min_date + datetime.timedelta(days=i)))
         for i in range(delta.days + 1)]

        self.log_files_to_use = sorted(list(set(self.log_files_to_use)))

    def find_all_logs_dashboard(self):
        """Use datetime to find all values between the min and max date,
        change those datetimes to strings, and append to the log_files_to_use_list
        This works for year, month, day like the logfile in survey profile data"""

        delta = self.max_date - self.min_date

        [self.log_files_to_use.append(self.datetime_strip_logfile_string(self.min_date + datetime.timedelta(days=i)))
         for i in range(delta.days + 1)]

        self.log_files_to_use = sorted(list(set(self.log_files_to_use)))

    @staticmethod
    def datetime_to_logfile_string(date):

        date = date.strftime("%Y%m%d")
        date = "surveyprofiledata-" + str(date).replace("-", "") + '.csv'
        return date

    @staticmethod
    def datetime_strip_logfile_string(date):

        date = str(date)
        last = date.rfind("-")
        date = date[:last]

        date = date.replace("-", ".") + '.csv'
        return date
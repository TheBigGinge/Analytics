import LogFileTools.log_iterator as li
import DateFunctions.datetimes_in as di
import FileHandling.file_work as fw
import csv
import collections
import numpy as np
import Statistics.entropy as stat
import datetime

log_file_path = '\\\\psfiler01\\data\\SurveyReports\\'
dash_path = '\\\\filer01\\public\\Data Dashboards\\'
unprompted_path = '\\\\filer01\\public\\Data_Analytics\\Job Rollup Suggesting\\Unprompted Strings Files\\'


class CreateUnpromptedStrings:

    def __init__(self):
        self.dates = di.DateTimeFormats()
        self.current_date = self.dates.find_first_of_current_month()
        self.current_unprompted = unprompted_path + self.current_date.strftime("%Y%m") + " Unprompted Strings List.csv"
        self.years_to_run = 2

        self.start_date = self.dates.find_first_of_month_x_years_ago(self.years_to_run)
        #self.start_date = datetime.datetime(2014, 10, 30)
        self.overall_list = []
        self.individual_list = []
        self.final_dict = {}
        self.individual_dict = {}
        self.individual_length = None
        self.header = ['Job Chosen', 'Unprompted String', 'Joint Count', 'CFM Count', 'UNC Count', 'Mutual Information',
                       'Word Similarity Score']

    def gather_data(self):

        logs = li.CSVLogIterator(self.start_date, self.current_date)
        logs.find_all_logs_survey()
        file_run = sorted(logs.log_files_to_use)

        handler = fw.FileHandler()

        for files in file_run:
            try:
                print "Working on " + files
                for row in handler.open_csv(log_file_path + files):
                    try:
                        final_job = row[handler.header.index("Profile job")]
                        unprompted_1 = row[handler.header.index('Profile job.unprompted')]
                        unprompted_2 = row[handler.header.index('Job\Job Unprompted')]
                        final_unprompted = self.determine_unprompted(unprompted_1, unprompted_2)
                        combined = final_job, final_unprompted
                        if "" not in combined:
                            self.overall_list.append(combined)
                            self.individual_list.append(final_job)
                            self.individual_list.append(final_unprompted)
                    except ValueError:
                        continue

            except IOError:
                continue

        print "File data completely gathered"

    @staticmethod
    def determine_unprompted(unprompted_1, unprompted_2):
        if unprompted_2 == "":
            return unprompted_1
        else:
            return unprompted_2

    def create_dictionaries(self):
        print "Getting counts for the probability distribution..."
        self.final_dict = collections.Counter(self.overall_list)
        self.individual_dict = collections.Counter(self.individual_list)
        self.individual_length = len(self.individual_list)

    def create_unprompted_file(self):
        print "Writing to file and calculating entropies..."
        with open(self.current_unprompted, 'wb') as W:
            writer = csv.writer(W, lineterminator='\n')
            writer.writerow(self.header)

            for keys in self.final_dict:
                if self.final_dict[keys] > 1:
                    np.seterr(invalid='raise')
                    try:
                        entropy = stat.joint_entropy(keys[0], keys[1]) / stat.entropy(keys[0])
                        mutual_info = stat.point_mutual_info(self.final_dict[keys],
                                                             self.individual_dict[keys[0]],
                                                             self.individual_dict[keys[1]],
                                                             self.individual_length)
                        final_row = keys[0], keys[1], self.final_dict[keys],\
                            self.individual_dict[keys[0]], self.individual_dict[keys[1]], mutual_info, entropy
                        writer.writerow(final_row)

                    except FloatingPointError:
                        entropy = float(1.0)
                        mutual_info = stat.point_mutual_info(self.final_dict[keys],
                                                             self.individual_dict[keys[0]],
                                                             self.individual_dict[keys[1]],
                                                             self.individual_length)
                        final_row = keys[0], keys[1], self.final_dict[keys],\
                            self.individual_dict[keys[0]], self.individual_dict[keys[1]], mutual_info, entropy
                        writer.writerow(final_row)

                    except ZeroDivisionError:
                        print keys, self.final_dict[keys]
                        continue
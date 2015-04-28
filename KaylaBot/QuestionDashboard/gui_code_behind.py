import os
import getpass
import csv
import datetime

from KaylaBot.QuestionDashboard import question_database as db
import LogFileTools.log_iterator as li
import DateFunctions.datetimes_in as dat
import FileHandling.file_work as fw


auto_path = "\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\"
local_path = os.path.expanduser("~" + getpass.getuser()) + "\\desktop\\"
output_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\output_files\\"


class QuestionDashSupport:

    def __init__(self):
        self.main_file_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\"

    @staticmethod
    def future_date_check(start_date):

        check = start_date.date()
        month = str(check.month())
        year = str(check.year())
        final_start = int(year + month)

        now = datetime.datetime.now()
        curr_month = str(now.month)
        curr_year = str(now.year)
        final_compare = int(curr_year + curr_month)

        if final_start >= final_compare:
            return False
        else:
            return True

    @staticmethod
    def soc_code_map():

        onet_mapping = {}
        main_file = fw.FileHandler()

        for row in main_file.open_csv(auto_path + "CFM.csv"):
            job = row[main_file.header.index("All Confirmed Job Titles")]
            soc = row[main_file.header.index("SOC Code")]
            onet_mapping[job] = soc

        return onet_mapping

    @staticmethod
    def count_number_of_files_to_process(start_date):

        survey_files = li.CSVLogIterator(dat.DateTimeFormats().date_to_date_time(start_date.date()),
                                         dat.DateTimeFormats().return_datetime_y_m_d_last_day_month(start_date.date()))

        survey_files.find_all_logs_survey()
        files_to_go = 0
        for survey in survey_files.log_files_to_use:
            files_to_go += 1

        return files_to_go

    def get_all_the_questions(self):

        all_questions = []

        with open(self.main_file_path + 'All_Questions.csv', 'rb') as R:
            reader = csv.reader(R, delimiter=',')

            [all_questions.append(row[0]) for row in reader if row[0] != 'All Questions']

        return all_questions

    @staticmethod
    def fill_all_breadth_db(start_date):

        for value in ['30', '40', '50', '60']:
            db.QuestionDashboardData().data_to_breadth_x_db(start_date, value)
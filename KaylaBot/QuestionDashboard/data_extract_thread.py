import zipfile
import os
import csv

from PyQt4 import QtCore

from KaylaBot.QuestionDashboard import question_database as db
import question_query_que as qat
import AnalysisTool.extract_data_xml as extract
import DateFunctions.datetimes_in as dat
import LogFileTools.log_iterator as logs
import gui_code_behind as cb


output_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\output_files\\"


class ExtractDataThread(QtCore.QThread):

    update_progress = QtCore.pyqtSignal(int)
    update_string_progress = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.log_path = '\\\\psfiler01\\data\\SurveyReports\\'
        self.denominator_dict = {}
        self.xml_handler = None
        self.start_date = None
        self.numerator_dict = {}
        self.numerator_compare = None
        self.denominator_compare = None
        self.soc_map = cb.QuestionDashSupport().soc_code_map()
        self.zip_file_name = "Kayla Question Activation Counts.zip"

    def get_date(self, this_date):

        self.start_date = this_date
        self.numerator_compare = self.start_date.date().toPyDate().strftime("%Y%m")
        self.denominator_compare = self.start_date.date().toPyDate().strftime("%Y%m%d")

    def run(self):

        #print self.numerator_compare
        if int(self.numerator_compare) not in db.QuestionDashboardData().get_all_dates():
            if cb.QuestionDashSupport().future_date_check(self.start_date):
                self.post_analysis_tool_and_extract_data()
                self.run_log_file_data_extraction()
            else:
                self.update_string_progress.emit("You cannot run data for this month or for the future.")

        else:
            self.update_string_progress.emit("This Data has been previously pulled.")

    def post_analysis_tool_and_extract_data(self):

        self.clean_files()
        self.update_string_progress.emit("Starting Analysis Tool call...")
        qat.BuildQueries(self.start_date.date()).main_query_build()
        self.unzip_file(self.zip_file_name)
        self.update_string_progress.emit("Analysis Tool call completed. Extracting data from xml...")

        self.pull_xml_data_to_dict(self.start_date)
        self.update_string_progress.emit("Analysis Tool segment complete")

    @staticmethod
    def clean_files():

        for files in os.listdir(output_path):
            os.remove(output_path + files)

    @staticmethod
    def last_day_of_month(given_date):

        return dat.DateTimeFormats().return_y_m_d_last_day_of_month(given_date, "-")

    @staticmethod
    def last_datetime_day_of_month(given_date):

        return dat.DateTimeFormats().return_datetime_y_m_d_last_day_month(given_date).date()

    @staticmethod
    def unzip_file(zip_file):
        #TODO: Make this method appear in file handling and replace this method and the one in Data Dist

        full_zip_file = zipfile.ZipFile(output_path + zip_file)
        file_list = full_zip_file.namelist()

        [full_zip_file.extract(file_name, output_path) for file_name in file_list]

    def pull_xml_data_to_dict(self, start_date):
        all_files = os.listdir(output_path)

        for files in all_files:
            if '.zip' not in files:
                extract.ExtractXMLData(files).fix_xml_encoding(output_path)
                self.xml_handler = extract.ExtractXMLData(output_path + files).row_name_entry_handler(header=True)
                self.change_dict_values()

    def change_dict_values(self):

        for question in cb.QuestionDashSupport().get_all_the_questions():
            question = question.replace("/", "_").replace(" ", "_").replace("-", "_")
            self.numerator_dict[question] = {}

        for key_value in self.xml_handler.count_dictionary:

            question = self.xml_handler.title_header.replace("/", "_").replace(" ", "_").replace("-", "_")
            onet = key_value[key_value.find("/PayScale Code ") + len("/PayScale Code "):].strip()
            target_count = self.xml_handler.count_dictionary[key_value]
            self.numerator_dict[question][onet] = target_count

    @staticmethod
    def date_format(date):
        return str(date.date().toPyDate())

    def run_log_file_data_extraction(self):

        log_files = logs.CSVLogIterator(self.start_date.date().toPyDate(),
                                        self.last_datetime_day_of_month(self.start_date.date()))
        log_files.find_all_logs_survey()

        for current_file_number, log_file in enumerate(log_files.log_files_to_use):
            self.update_string_progress.emit("Working on " + log_file + "...")
            with open(self.log_path + log_file, 'rb') as R:
                reader = csv.reader(R, delimiter=',')
                header = reader.next()

                for row in reader:

                    saw_20 = row[header.index("Saw20")]
                    bailed_20 = row[header.index("Bailed20")]
                    saw_payscale = row[header.index("SawMyPayscale")]
                    profile_job = row[header.index("Profile job")]
                    try:
                        soc = self.soc_map[profile_job]
                    except KeyError:
                        soc = "N/A"
                    self.log_data_to_dictionary(row, header, saw_20, bailed_20, saw_payscale, soc)

            self.update_progress.emit(current_file_number + 1)

        self.update_string_progress.emit("Log File data completely gathered")
        self.update_string_progress.emit("Placing log data and Analysis Tool data into database...")
        db.QuestionDashboardData().insert_data_from_dict_to_database(self.denominator_dict,
                                                                     self.numerator_dict,
                                                                     self.start_date.date().toPyDate().
                                                                     strftime("%Y%m"))

        self.update_string_progress.emit("Filling up the different breadth x databases...")
        cb.QuestionDashSupport().fill_all_breadth_db(self.start_date.date().toPyDate().strftime("%Y%m"))

        self.update_string_progress.emit("Log File and Analysis Tool work completed. Feel free to query away on the"
                                         "currently pulled months data.")

    def data_to_dict(self, question, soc, value):

        try:
            self.denominator_dict[question][soc][value] += 1
        except KeyError:
            try:
                self.denominator_dict[question][soc][value] = 1
            except KeyError:
                try:
                    self.denominator_dict[question][soc] = {}
                    self.denominator_dict[question][soc][value] = 1
                except KeyError:
                    self.denominator_dict[question] = {}
                    self.denominator_dict[question][soc] = {}
                    self.denominator_dict[question][soc][value] = 1

    def log_data_to_dictionary(self, row, header, saw_20, bailed_20, saw_payscale, soc):

        all_questions = cb.QuestionDashSupport().get_all_the_questions()

        for question in all_questions:
            try:
                field_shown = row[header.index(question)]
            except ValueError:
                field_shown = 'no_answer'

            if field_shown == 'Field Shown':
                self.data_to_dict(question, soc, 'total_shown')

            if saw_20.lower() == "true" and field_shown == 'Field Shown':
                self.data_to_dict(question, soc, 'saw_20')

            if bailed_20.lower() == 'true' and field_shown == 'Field Shown':
                self.data_to_dict(question, soc, 'bailed_20')

            if saw_payscale.lower() == 'true' and field_shown == 'Field Shown':
                self.data_to_dict(question, soc, 'saw_payscale')
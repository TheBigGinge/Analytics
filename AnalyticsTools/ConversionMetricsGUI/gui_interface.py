import os
import datetime
import getpass
import csv

from PyQt4 import QtCore, QtGui

from AnalyticsTools.ConversionMetricsGUI import file_cycle
import database
import Statistics.chi_square as stats


local_path = os.path.expanduser("~" + getpass.getuser()) + "\\desktop\\"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

data_path = '\\\\pssea\\files\\public\\Data Analytics\\Consumer Log Metrics\\Data Files\\'
log_path_write = '\\\\pssea\\files\\public\\Data Analytics\\Consumer_Level_Conversion\\'
log_path = '\\\\psfiler01\\data\\SurveyReports\\'
alert_path = '\\\\filer01\\public\\Data_Analytics\\Consumer_Level_Conversion\\Alert_Files\\'


class UIForm(object):

    def __init__(self):
        super(UIForm, self).__init__()
        self.export_name = "Level Conversion Output.csv"
        self.comparison_export_name = "Level Conversion Comparison.csv"
        self.all_consumer_logs = os.listdir(log_path)
        self.log_files_already_used = database.DataBaseQueries.pull_all_used_dates()
        self.first_survey_type = []
        self.second_survey_type = []
        self.fancy_progress_bar = None
        self.compare_to_csv = False
        self.first_period = None
        self.second_period = None
        self.work_thread = None
        self.survey_type = []
        self.final_counts = None
        self.last_date = None
        self.begin_function = False
        self.to_csv = False
        self.start_label = None
        self.to_csv_button = None
        self.yes_button = None
        self.compare_button = None
        self.end_label = None
        self.text_edit = None
        self.current_job_check = None
        self.current_job_edit_check = None
        self.job_offer_check = None
        self.start_date = None
        self.end_date = None
        self.get_data_button = None
        self.main_text_browser = None
        self.final_counts_first = None
        self.final_counts_second = None
        self.progress_label = None
        self.reset_compare_count = 0

    def setup_ui(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(640, 480)
        self.current_job_check = QtGui.QCheckBox(Form)
        self.current_job_check.setGeometry(QtCore.QRect(520, 60, 81, 17))
        self.current_job_check.setObjectName(_fromUtf8("checkBox"))

        self.current_job_edit_check = QtGui.QCheckBox(Form)
        self.current_job_edit_check.setGeometry(QtCore.QRect(520, 90, 101, 17))
        self.current_job_edit_check.setObjectName(_fromUtf8("checkBox_2"))

        self.job_offer_check = QtGui.QCheckBox(Form)
        self.job_offer_check.setGeometry(QtCore.QRect(520, 120, 70, 17))
        self.job_offer_check.setObjectName(_fromUtf8("checkBox_3"))

        self.start_date = QtGui.QDateEdit(Form)
        self.start_date.setGeometry(QtCore.QRect(390, 60, 110, 22))
        self.start_date.setObjectName(_fromUtf8("dateEdit"))
        self.start_date.setDate(QtCore.QDate.fromString('01.01.2014', 'MM.dd.yyyy'))

        self.end_date = QtGui.QDateEdit(Form)
        self.end_date.setGeometry(QtCore.QRect(390, 120, 110, 22))
        self.end_date.setObjectName(_fromUtf8("dateEdit_2"))
        self.end_date.setDate(QtCore.QDate.fromString('01.02.2014', 'MM.dd.yyyy'))

        self.get_data_button = QtGui.QPushButton(Form)
        self.get_data_button.setGeometry(QtCore.QRect(520, 160, 111, 23))
        self.get_data_button.setObjectName(_fromUtf8("pushButton"))

        self.fancy_progress_bar = QtGui.QProgressBar(Form)
        self.fancy_progress_bar.setGeometry(QtCore.QRect(30, 70, 331, 41))
        self.fancy_progress_bar.setProperty("value", 24)
        self.work_thread = file_cycle.ReadLogFiles(self.all_consumer_logs, self.log_files_already_used)
        self.work_thread.update_string_progress.connect(self.set_string_progress)
        self.work_thread.update_progress.connect(self.set_progress)

        self.main_text_browser = QtGui.QScrollArea(Form)
        self.main_text_browser.setGeometry(QtCore.QRect(30, 180, 471, 191))
        self.main_text_browser.setObjectName(_fromUtf8("textBrowser"))
        self.text_edit = QtGui.QTextEdit()
        self.text_edit.setGeometry(QtCore.QRect(30, 180, 471, 191))
        self.main_text_browser.setWidget(self.text_edit)

        self.get_data_button.clicked.connect(self.get_the_data_button)

        self.start_label = QtGui.QLabel(Form)
        self.start_label.setGeometry(QtCore.QRect(390, 40, 51, 16))
        self.start_label.setObjectName(_fromUtf8("label"))
        self.end_label = QtGui.QLabel(Form)
        self.end_label.setGeometry(QtCore.QRect(390, 100, 46, 13))
        self.end_label.setObjectName(_fromUtf8("label_2"))

        self.progress_label = QtGui.QLabel(Form)
        self.progress_label.setGeometry(QtCore.QRect(30, 30, 131, 21))
        self.progress_label.setObjectName(_fromUtf8("label_3"))

        self.to_csv_button = QtGui.QPushButton(Form)
        self.to_csv_button.setGeometry(QtCore.QRect(30, 400, 75, 23))
        self.to_csv_button.setObjectName(_fromUtf8("pushButton_2"))
        self.compare_button = QtGui.QPushButton(Form)
        self.compare_button.setGeometry(QtCore.QRect(520, 200, 111, 31))
        self.compare_button.setObjectName(_fromUtf8("pushButton_3"))
        self.yes_button = QtGui.QPushButton(Form)
        self.yes_button.setGeometry(QtCore.QRect(430, 400, 75, 23))
        self.yes_button.setObjectName(_fromUtf8("pushButton_4"))

        self.to_csv_button.clicked.connect(self.write_to_csv)
        self.compare_button.clicked.connect(self.compare_the_data_button)

        self.re_translate_ui(Form)

        self.fancy_progress_bar.setRange(0, self.get_remaining_files())
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.begin()

    def re_translate_ui(self, Form):
        Form.setWindowTitle(_translate("Form", "Level Conversion Analysis", None))
        self.current_job_check.setText(_translate("Form", "CurrentJob", None))
        self.current_job_edit_check.setText(_translate("Form", "CurrentJob-Edit", None))
        self.job_offer_check.setText(_translate("Form", "JobOffer", None))
        self.get_data_button.setText(_translate("Form", "Show Me the Data!", None))
        self.start_label.setText(_translate("Form", "Start Date", None))
        self.end_label.setText(_translate("Form", "End Date", None))
        self.to_csv_button.setText(_translate("Form", "To Csv", None))
        self.compare_button.setText(_translate("Form", "Compare Data", None))
        self.yes_button.setText(_translate("Form", "Update Data", None))
        self.progress_label.setText(_translate("Form", "Log File Update Progress", None))
        self.fancy_progress_bar.setValue(0)
        self.yes_button.clicked.connect(self.work_thread.start)

    def set_progress(self, progress):

        self.fancy_progress_bar.setValue(progress)

    def set_string_progress(self, progress):

        self.text_edit.append(progress)

    def get_remaining_files(self):

        counter = 0

        for files in self.all_consumer_logs:
            if "surveyprofiledata" not in files:
                continue
            elif ".csv" not in files:
                continue
            elif "aggregate" in files:
                continue
            elif "old" in files:
                continue
            elif "2012" in files or "2013" in files or "2014" in files:
                continue
            elif files[len("surveyprofiledata-"): len("surveyprofiledata-") + 8] \
                    in self.log_files_already_used:
                    continue
            else:
                counter += 1

        return counter

    def get_the_data_button(self):

        start_time = self.start_date.date().toPyDate()
        end_time = self.end_date.date().toPyDate()

        start_time = str(start_time).replace("-", "")
        end_time = str(end_time).replace("-", "")

        if int(end_time) < int(start_time):
            self.text_edit.append("The end date needs to be greater than the start date \n")
            pass
        elif int(start_time) < 20130101:
            self.text_edit.append("The start date needs to be after 2013-01-01 \n")
        elif int(start_time) < 20130911 < int(end_time):
            self.text_edit.append("The first day the logs changed level_40 to level_20 was 2013-09-12. ")
            self.text_edit.append("This means that this range will have mixed values of level_20 and level_40. ")
            self.text_edit.append("I recommend setting a range that doesn't cross over the date 2013-09-11. \n")
        else:

            if self.current_job_check.isChecked() is True:
                self.survey_type.append("FastTrack")
            elif self.current_job_check.isChecked() is not True:
                try:
                    self.survey_type.remove("FastTrack")
                except ValueError:
                    pass

            if self.current_job_edit_check.isChecked() is True:
                self.survey_type.append("FastTrack_Edit")
            elif self.current_job_edit_check.isChecked() is not True:
                try:
                    self.survey_type.remove("FastTrack_Edit")
                except ValueError:
                    pass

            if self.job_offer_check.isChecked() is True:
                self.survey_type.append("JobOffer")
            elif self.job_offer_check.isChecked() is not True:
                try:
                    self.survey_type.remove("JobOffer")
                except ValueError:
                    pass

            if len(self.survey_type) == 0:
                self.text_edit.append("You need to choose at least one survey type first \n")
            else:
                self.final_counts = self.pull_data(start_time, end_time, False)

    def compare_the_data_button(self):

        start_time = self.start_date.date().toPyDate()
        end_time = self.end_date.date().toPyDate()

        start_time = str(start_time).replace("-", "")
        end_time = str(end_time).replace("-", "")

        if int(end_time) < int(start_time):
            self.text_edit.append("The end date needs to be greater than the start date \n")
            pass
        elif int(start_time) < 20130101:
            self.text_edit.append("The start date needs to be after 2013-01-01 \n")
        elif int(start_time) < 20130911 < int(end_time):
            self.text_edit.append("The first day the logs changed level_40 to level_20 was 2013-09-12. ")
            self.text_edit.append("This means that this range will have mixed values of level_20 and level_40. ")
            self.text_edit.append("I recommend setting a range that doesn't cross over the date 2013-09-11. \n")
        else:

            if self.current_job_check.isChecked() is True:
                self.survey_type.append("FastTrack")
            elif self.current_job_check.isChecked() is not True:
                try:
                    self.survey_type.remove("FastTrack")
                except ValueError:
                    pass

            if self.current_job_edit_check.isChecked() is True:
                self.survey_type.append("FastTrack_Edit")
            elif self.current_job_edit_check.isChecked() is not True:
                try:
                    self.survey_type.remove("FastTrack_Edit")
                except ValueError:
                    pass

            if self.job_offer_check.isChecked() is True:
                self.survey_type.append("JobOffer")
            elif self.job_offer_check.isChecked() is not True:
                try:
                    self.survey_type.remove("JobOffer")
                except ValueError:
                    pass

            if len(self.survey_type) == 0:
                self.text_edit.append("You need to choose at least one survey type first \n")
            else:
                if self.reset_compare_count == 0:
                    self.final_counts_first = self.pull_data(start_time, end_time, True)
                    self.first_period = str(self.start_date.date().toPyDate()) + " to " + \
                        str(self.end_date.date().toPyDate())
                    self.first_survey_type.extend(self.survey_type)
                    self.survey_type = []
                    self.reset_compare_count = 1

                elif self.reset_compare_count == 1:
                    self.compare_to_csv = True
                    self.final_counts_second = self.pull_data(start_time, end_time, True)
                    self.second_period = str(self.start_date.date().toPyDate()) + " to " + \
                        str(self.end_date.date().toPyDate())

                    self.second_survey_type.extend(self.survey_type)
                    self.survey_type = []
                    self.reset_compare_count = 2

    def pull_data(self, start_time, end_time, compare):

        dictionary_list = []
        final_counts = {}

        for surveys in self.survey_type:

            conversion = database.DataBaseQueries().pull_overall_data(start_time, end_time, surveys)
            conversion_20 = database.DataBaseQueries().pull_conversions_for_optional_levels('level_20',
                                                                                            surveys,
                                                                                            start_time, end_time)
            conversion_60 = database.DataBaseQueries().pull_conversions_for_optional_levels("level_60",
                                                                                            surveys,
                                                                                            start_time, end_time)
            conversion_80 = database.DataBaseQueries().pull_conversions_for_optional_levels("level_80",
                                                                                            surveys,
                                                                                            start_time, end_time)
            dictionary_list.append(conversion)
            dictionary_list.append(conversion_20)
            dictionary_list.append(conversion_60)
            dictionary_list.append(conversion_80)

        for i, dictionaries in enumerate(dictionary_list):
            if i == 0:

                final_counts = dictionaries

            else:

                final_counts = self.count_dictionaries(final_counts, dictionaries)
        if compare is False:
            self.to_csv = True
            self.text_edit.append("Your data has been pulled. If you'd like it to be exported to a csv file hit the "
                                  "To Csv button \n")
        elif compare is False and self.reset_compare_count == 1:
            self.text_edit.append("Your data has been pulled. If you'd like it to be exported to a csv file hit the "
                                  "To Csv button. The data you pulled for compare counts are now gone \n")
            self.reset_compare_count = 0
        elif compare is True and self.reset_compare_count == 0:
            self.text_edit.append("The first period of data has been pulled. Select a second period to compare it to "
                                  "and then press the Compare Data button again. \n")
        elif compare is True and self.reset_compare_count == 1:
            self.text_edit.append("Both periods are now ready for comparison. Press the To Csv button to get the"
                                  "results \n")
        elif compare == "pass":
            pass

        return final_counts

    @staticmethod
    def count_dictionaries(dictionary_1, dictionary_2):

        return_dictionary = {}

        key_list_1 = dictionary_1.keys()
        key_list_2 = dictionary_2.keys()

        for keys in key_list_1:
            if keys in key_list_2:
                top = dictionary_1[keys][0] + dictionary_2[keys][0]
                bottom = dictionary_1[keys][1] + dictionary_2[keys][1]

                return_dictionary[keys] = top, bottom
            else:
                return_dictionary[keys] = dictionary_1[keys]

        for keys in key_list_2:
            if keys not in key_list_1:
                return_dictionary[keys] = dictionary_2[keys]

        return return_dictionary

    def compare_data_to_csv(self, survey_string=None, final_counts_first=None, final_counts_second=None,
                            first_period_begin=None, yesterday=None, second_period_begin=None, second_period_end=None,
                            today=None):

        if survey_string is not None:
            self.alert_compare_data_to_csv(survey_string, final_counts_first, final_counts_second, first_period_begin,
                                           yesterday, second_period_begin, second_period_end, today)
        else:
            i = 0
            if self.compare_to_csv is True:
                self.first_survey_type = list(set(self.first_survey_type))
                self.second_survey_type = list(set(self.second_survey_type))
                first_survey_string = ""
                for z, surveys in enumerate(self.first_survey_type):
                    if z == 0 and len(self.first_survey_type) == 1:
                        first_survey_string += surveys
                    elif z == 0 and len(self.first_survey_type) != 1:
                        first_survey_string += surveys + ", "
                    elif z == len(self.first_survey_type) - 1:
                        first_survey_string += "and " + surveys
                    else:
                        first_survey_string += surveys + ", "

                second_survey_string = ""
                for x, surveys in enumerate(self.second_survey_type):

                    if x == 0 and len(self.second_survey_type) == 1:
                        second_survey_string += surveys
                    elif x == 0 and len(self.second_survey_type) != 1:
                        second_survey_string += surveys + ", "
                    elif x == len(self.second_survey_type) - 1:
                        second_survey_string += "and " + surveys
                    else:
                        second_survey_string += surveys + ", "

                while True:
                    if os.path.exists(local_path + self.comparison_export_name):
                        i += 1
                        self.comparison_export_name = "Level Conversion Comparison (%s).csv" % i
                    elif os.path.exists(local_path + self.comparison_export_name) is False:
                        break
                try:
                    with open(local_path + self.comparison_export_name, 'w') as R:
                        writer = csv.writer(R, lineterminator='\n')

                        names = [first_survey_string + " for the time period of " + self.first_period,
                                 "Numerator", "Denominator", "Percentage", second_survey_string +
                                 " for the time period of " + self.second_period, "Numerator", "Denominator", "Percentage",
                                 "Chi-Square", "P-Value"]

                        writer.writerow(names)

                        for keys in self.final_counts_first:

                            first_numerator = self.final_counts_first[keys][0]
                            first_denominator = self.final_counts_first[keys][1]
                            second_numerator = self.final_counts_second[keys][0]
                            second_denominator = self.final_counts_second[keys][1]

                            observed_list = [first_numerator, first_denominator - first_numerator, second_numerator,
                                             second_denominator - second_numerator]
                            statistics = stats.ChiSquaredIndependence(observed_list).calculate_chi_square()

                            try:
                                first_ratio = float(first_numerator) / float(first_denominator)
                            except ZeroDivisionError:
                                first_ratio = 0

                            try:
                                second_ratio = float(second_numerator) / float(second_denominator)
                            except ZeroDivisionError:
                                second_ratio = 0

                            line = keys, first_numerator, first_denominator, first_ratio, keys, second_numerator, \
                                second_denominator, second_ratio, statistics[0], statistics[1]

                            writer.writerow(line)

                    self.compare_to_csv = False
                    self.text_edit.append("Exported " + local_path + self.comparison_export_name + " \n")

                except IOError:
                    i += 1
                    self.comparison_export_name = "Level Conversion Comparison (%s).csv" % i
                    with open(local_path + self.comparison_export_name, 'w') as R:
                        writer = csv.writer(R, lineterminator='\n')

                        names = [first_survey_string + " for the time period of " + self.first_period,
                                 "Numerator", "Denominator", "Percentage", second_survey_string +
                                 " for the time period of " + self.second_period, "Numerator", "Denominator", "Percentage",
                                 "Chi-Square", "P-Value"]

                        writer.writerow(names)

                        for keys in self.final_counts_first:

                            first_numerator = self.final_counts_first[keys][0]
                            first_denominator = self.final_counts_first[keys][1]
                            second_numerator = self.final_counts_second[keys][0]
                            second_denominator = self.final_counts_second[keys][1]

                            observed_list = [first_numerator, first_denominator - first_numerator, second_numerator,
                                             second_denominator - second_numerator]
                            statistics = stats.ChiSquaredIndependence(observed_list).calculate_chi_square()

                            try:
                                first_ratio = float(first_numerator) / float(first_denominator)
                            except ZeroDivisionError:
                                first_ratio = 0

                            try:
                                second_ratio = float(second_numerator) / float(second_denominator)
                            except ZeroDivisionError:
                                second_ratio = 0

                            line = keys, first_numerator, first_denominator, first_ratio, keys, second_numerator, \
                                second_denominator, second_ratio, statistics[0], statistics[1]

                            writer.writerow(line)

                    self.text_edit.append("Exported " + local_path + self.comparison_export_name + " \n")
                    self.compare_to_csv = False
                    i += 1

            else:
                print "Nope"

    def write_to_csv(self):

        if self.to_csv is True:

            start_time = self.start_date.date().toPyDate()
            end_time = self.end_date.date().toPyDate()
            start_time = str(start_time)
            end_time = str(end_time)
            x = 1

            survey_string = ""
            self.survey_type = list(set(self.survey_type))
            for i, surveys in enumerate(self.survey_type):
                if i == 0 and len(self.survey_type) == 1:
                    survey_string += surveys
                elif i == 0 and len(self.survey_type) != 1:
                    survey_string += surveys + ", "
                elif i == len(self.survey_type) - 1:
                    survey_string += "and " + surveys
                else:
                    survey_string += surveys + ", "

            while True:
                if os.path.exists(local_path + self.export_name):
                    x += 1
                    self.export_name = "Level Conversion Output (%s).csv" % x
                elif os.path.exists(local_path + self.export_name) is False:
                    break

            try:

                with open(local_path + self.export_name, 'w') as R:
                    writer = csv.writer(R, lineterminator='\n')

                    names = ["Ratio", "Numerator", "Denominator", "Percentage", "For the time period between "
                                                                                + start_time
                             + " and " + end_time, survey_string]

                    writer.writerow(names)

                    for keys in self.final_counts:

                        numerator = self.final_counts[keys][0]
                        denominator = self.final_counts[keys][1]

                        if denominator == 0:
                            continue
                        else:
                            try:
                                ratio = float(numerator) / float(denominator)
                            except ZeroDivisionError:
                                ratio = 0

                            line = keys, numerator, denominator, ratio

                            writer.writerow(line)

                self.text_edit.append("Exported " + local_path + self.export_name + " \n")
                self.to_csv = False

            except IOError:
                x += 1
                self.export_name = "Level Conversion Output (%s).csv" % x
                with open(local_path + self.export_name, 'w') as R:
                    writer = csv.writer(R, lineterminator='\n')

                    names = ["Ratio", "Numerator", "Denominator", "Percentage", "For the time period between " +
                             start_time + " and " + end_time, survey_string]

                    writer.writerow(names)

                    for keys in self.final_counts:

                        numerator = self.final_counts[keys][0]
                        denominator = self.final_counts[keys][1]
                        ratio = float(numerator) / float(denominator)

                        line = keys, numerator, denominator, ratio

                        writer.writerow(line)

                self.text_edit.append("Exported " + local_path + self.export_name + " \n")
                self.to_csv = False
                x += 1

        elif self.compare_to_csv is True:
            self.compare_data_to_csv()
        else:
            print "Nope"

    def begin(self):

        #Pull the most current date from the database
        last_date = database.DataBaseQueries.pull_max_date()
        last_date = str(last_date)
        self.last_date = last_date

        year = last_date[:4]
        month = last_date[4:6]
        day = last_date[6:8]

        last_used_date = str(year) + "-" + str(month) + "-" + str(day)

        self.text_edit.append("Welcome to the Level Conversion Metrics Tool, " + getpass.getuser() + " \n")
        self.text_edit.append("All conversion counts are currently up to date through " + last_used_date + " \n")

        if self.current_date_check() is True:
            self.text_edit.append("Which means all log files are currently updated at this time \n")
        else:

            self.text_edit.append("If you need to update the counts to the current date to complete "
                                  "your analysis press the update data button now \n")
            self.begin_function = True

    @staticmethod
    def current_date_check():

        now = datetime.datetime.now()

        yesterday = now - datetime.timedelta(days=1)

        yesterday = str(yesterday)[:10].replace("-", "")

        compare = database.DataBaseQueries.pull_max_date()
        compare = str(compare)

        if compare == yesterday:
            result = True
        else:
            result = False

        return result

    def get_text_edit(self):

        return self.text_edit

    @staticmethod
    def alert_compare_data_to_csv(survey_string, final_counts_first, final_counts_second, first_period_begin,
                                  yesterday, second_period_begin, second_period_end, today):

        comparison_export_name = survey_string + "_" + today + "_Conversion_Alert_Comparison.csv"

        first_period = first_period_begin + " to " + yesterday
        second_period = second_period_begin + " to " + second_period_end

        with open(alert_path + comparison_export_name, 'wb') as R:
            writer = csv.writer(R, lineterminator='\n')

            names = [survey_string + " for the time period of " + first_period,
                     "Numerator", "Denominator", "Percentage", survey_string +
                     " for the time period of " + second_period, "Numerator", "Denominator", "Percentage",
                     "Chi-Square", "P-Value"]

            writer.writerow(names)

            for keys in final_counts_first:

                first_numerator = final_counts_first[keys][0]
                first_denominator = final_counts_first[keys][1]
                second_numerator = final_counts_second[keys][0]
                second_denominator = final_counts_second[keys][1]

                observed_list = [first_numerator, first_denominator - first_numerator, second_numerator,
                                 second_denominator - second_numerator]

                statistics = stats.ChiSquaredIndependence(observed_list).calculate_chi_square()

                try:
                    first_ratio = float(first_numerator) / float(first_denominator)
                except ZeroDivisionError:
                    first_ratio = 0

                try:
                    second_ratio = float(second_numerator) / float(second_denominator)
                except ZeroDivisionError:
                    second_ratio = 0

                line = keys, first_numerator, first_denominator, first_ratio, keys, second_numerator, \
                    second_denominator, second_ratio, statistics[0], statistics[1]

                writer.writerow(line)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = UIForm()
    ui.setup_ui(Form)
    Form.show()
    sys.exit(app.exec_())
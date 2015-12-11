import csv
import sqlite3
import time
from Constants import constant_strings as c
from PyQt4 import QtCore

from AnalyticsTools.ConversionMetricsGUI import levels
from database import DataBaseQueries as dbq

constant = c.Constants()
log_path = constant.log_path
log_path_write = constant.consumer_level_conversion


class ReadLogFiles(QtCore.QThread):

    relevant_files = []
    update_progress = QtCore.pyqtSignal(int)
    update_string_progress = QtCore.pyqtSignal(str)

    def __init__(self, all_consumer_logs, log_files_already_used):
        QtCore.QThread.__init__(self)
        #self.last_updated_date = last_updated_date
        self.all_consumer_logs = all_consumer_logs
        self.log_files_already_used = log_files_already_used
        self.who_cares = ['Informational', 'Informational-Edit', 'JobOffer-Edit']
        self.relevant_logs()
        self.names = None
        self.month_counts = {}
        #self.pull_log_data()

    def relevant_logs(self):

        #getting rid of the crap I don't need from the logs folder
        #and then not using any files that have already been processed

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
                ReadLogFiles.relevant_files.append(files)

    def log_line_pull(self, log_file_name):

        with open(log_path + log_file_name, 'rb') as R:
            reader = csv.reader(R, delimiter=',')

            self.names = reader.next()

            for row in reader:
                yield row

    @staticmethod
    def add_value_to_dictionary(temp_count_dict, surveys_name, survey_level):

        #Adding counts to the dictionary for specified fields
        #Adds a count or creates the keys in the dictionary with a value set at 1
        try:
            temp_count_dict[surveys_name][survey_level] += 1
        except KeyError:
            if surveys_name not in temp_count_dict.keys():
                temp_count_dict[surveys_name] = {}
                temp_count_dict[surveys_name][survey_level] = 1
            else:
                temp_count_dict[surveys_name][survey_level] = 1

    @staticmethod
    def add_value_to_level_dictionary(temp_level_count_dict, surveys_name, survey_level, base_level):

        #Adding counts to the dictionary for specified fields
        #Adds a count or creates the keys in the dictionary with a value set at 1
        main_key = base_level.replace("SurveyLevel ", "").replace("FastTrack-Edit", "Level").\
        replace("FastTrack", "Level").replace("JobOffer", "Level")

        try:
            temp_level_count_dict[main_key][surveys_name][survey_level] += 1
        except KeyError:
            if main_key not in temp_level_count_dict.keys():
                temp_level_count_dict[main_key] = {}
                temp_level_count_dict[main_key][surveys_name] = {}
                temp_level_count_dict[main_key][surveys_name][survey_level] = 1
            else:
                if surveys_name not in temp_level_count_dict[main_key].keys():
                    temp_level_count_dict[main_key][surveys_name] = {}
                    temp_level_count_dict[main_key][surveys_name][survey_level] = 1
                else:
                    if survey_level not in temp_level_count_dict[main_key][surveys_name].keys():
                        temp_level_count_dict[main_key][surveys_name][survey_level] = 1

    @staticmethod
    def add_completion_to_level_dictionary(temp_level_count_dict, surveys_name, base_level):

        main_key = base_level.replace("SurveyLevel ", "").replace("FastTrack-Edit", "Level").\
        replace("FastTrack", "Level").replace("JobOffer", "Level")

        try:
            temp_level_count_dict[main_key][surveys_name]["SawMyPayScale"] += 1
        except KeyError:
            if main_key not in temp_level_count_dict.keys():
                temp_level_count_dict[main_key] = {}
                temp_level_count_dict[main_key][surveys_name] = {}
                temp_level_count_dict[main_key][surveys_name]["SawMyPayScale"] = 1
            else:
                if surveys_name not in temp_level_count_dict[main_key].keys():
                    temp_level_count_dict[main_key][surveys_name] = {}
                    temp_level_count_dict[main_key][surveys_name]["SawMyPayScale"] = 1
                else:
                    if "SawMyPayScale" not in temp_level_count_dict[main_key][surveys_name].keys():
                        temp_level_count_dict[main_key][surveys_name]["SawMyPayScale"] = 1

    @staticmethod
    def add_completion_value_to_dictionary(temp_count_dict, surveys_name):

        #only for the SawMyPaysScale field in the surveys
        try:
            temp_count_dict[surveys_name]["SawMyPayScale"] += 1
        except KeyError:
            if surveys_name not in temp_count_dict.keys():
                temp_count_dict[surveys_name] = {}
                temp_count_dict[surveys_name]["SawMyPayScale"] = 1
            else:
                temp_count_dict[surveys_name]["SawMyPayScale"] = 1

    @staticmethod
    def key_try(temp_count_dict, keys, level):

        try:
            final = temp_count_dict[keys][level]
        except KeyError:
            final = 0

        return final

    @staticmethod
    def level_key_try(temp_level_count_dict, keys, second_keys, specified_level):
        try:
            final = temp_level_count_dict[keys][second_keys][specified_level]
        except KeyError:
            final = 0

        return final

    def count_survey_levels(self, all_survey_levels, levels_to_use, survey_type, temp_count_dict):

        for i, true_false in enumerate(all_survey_levels):

            #early versions of the consumer logs don't contain any of the -edit job survey types
            try:

                surveys_stripped = levels_to_use[i].replace("SurveyLevel ", "")

                #surveys_name is the name from levels.all_levels with the -15 or -20 sliced off
                #surveys_name is used to match to the survey name from the logs
                surveys_name = surveys_stripped[:len(surveys_stripped) - 3]

                #surveys level is the level of the survey from levels.all_levels
                survey_level = surveys_stripped[len(surveys_stripped) - 2:]
                survey_level = "level_" + survey_level

                if survey_type == surveys_name and true_false.lower() == "true":

                    self.add_value_to_dictionary(temp_count_dict, surveys_name, survey_level)

            except ValueError:
                return

    def optional_level_counter(self, base_level_survey_levels, levels_to_use, survey_type, temp_level_count_dict,
                               base_question_position, survey_finish):

        for i, true_false in enumerate(base_level_survey_levels):

            if base_level_survey_levels[0].lower() != "true":
                break

            else:

                #early versions of the consumer logs don't contain any of the -edit job survey types
                try:

                    surveys_stripped = levels_to_use[i + base_question_position].replace("SurveyLevel ", "")

                    #surveys_name is the name from levels.all_levels with the -15 or -20 sliced off
                    #surveys_name is used to match to the survey name from the logs
                    surveys_name = surveys_stripped[:len(surveys_stripped) - 3]

                    #surveys level is the level of the survey from levels.all_levels
                    survey_level = surveys_stripped[len(surveys_stripped) - 2:]
                    survey_level = "level_" + survey_level

                    if survey_type == surveys_name and true_false.lower() == "true":

                        self.add_value_to_level_dictionary(temp_level_count_dict, surveys_name,
                                                           survey_level, levels_to_use[base_question_position])

                    if survey_finish.lower() == "true" and i == 0:
                        self.add_completion_to_level_dictionary(temp_level_count_dict, surveys_name,
                                                                levels_to_use[base_question_position])

                except ValueError:
                    return

    def find_survey_values(self, iterator, levels_to_use, value_in_list):

        #Find the True / False value of the survey level and if the particular survey level
        #doesn't exist return N/A so that a test later on that uses .lower() won't break on an int
        try:
            survey_level = iterator[self.names.index(levels_to_use[value_in_list])]
        except ValueError:
            survey_level = "N/A"
        return survey_level

    @staticmethod
    def check_for_real_survey_finish(required_levels):

        #In order for a survey to actually be complete you need to have completed all of the
        #required fields. This makes sure all the required fields were completed
        final_answer = True

        for needed_fields in required_levels:
            if needed_fields.lower() != "true":
                final_answer = False
                break
            else:
                continue

        return final_answer

    def run(self):

        #Main method containing all of the rules for going through the individual log files
        #and manipulating the data

        #Temp count dict holds all the counts for this individual log file
        #Once the log file has been completely read the temp count dict values are sent to a sql_lite database
        #and the count dict is emptied at the end
        temp_count_dict = {}
        temp_level_count_dict = {}

        self.update_string_progress.emit("Pulling log data now... \n")

        for current_file_number, log_file in enumerate(ReadLogFiles.relevant_files):

            date = log_file[18:26]
            current_year = date[:4]
            current_month = date[4:6]
            current_day = date[6:8]

            final_date = current_month + "-" + current_day + "-" + current_year
            use_date = current_year + current_month + current_day

            #text_edit = self.get_text_edit()

            #self.ui.text_edit.append("Working on the file for %s" % final_date)
            print "Working on the file for %s" % final_date

            current_file = self.log_line_pull(log_file)

            for i, lines in enumerate(current_file):

                if i % 5000 == 0 and i != 0:
                    #self.text_edit.append("%s lines processed..." % i)
                    print "%s lines processed..." % i

                #Due to inconsistent naming in the log headers I'm choosing FasTrack as the
                #chosen terminology of SurveyType
                survey_type = lines[self.names.index("SurveyType")]
                survey_type = survey_type.replace("CurrentJob", "FastTrack")

                survey_finish = lines[self.names.index("SawMyPayscale")]
                levels_to_use = None

                #Find which survey levels to use based on survey type
                if "FastTrack" in survey_type and "Edit" not in survey_type:
                    levels_to_use = levels.fast_track_levels
                elif "FastTrack" in survey_type and "Edit" in survey_type:
                    levels_to_use = levels.fast_track_edit_levels
                elif "JobOffer" in survey_type:
                    levels_to_use = levels.job_offer_levels
                else:
                    continue

                survey_level_test = "SurveyLevel " + survey_type + "-15"

                if survey_level_test in self.names:
                    level_type = "15"
                else:
                    level_type = "40"

                check_15 = self.find_survey_values(lines, levels_to_use, 0)
                check_20 = self.find_survey_values(lines, levels_to_use, 1)
                check_30 = self.find_survey_values(lines, levels_to_use, 2)
                check_50 = self.find_survey_values(lines, levels_to_use, 3)
                check_60 = self.find_survey_values(lines, levels_to_use, 4)
                check_70 = self.find_survey_values(lines, levels_to_use, 5)
                check_80 = self.find_survey_values(lines, levels_to_use, 6)
                check_90 = self.find_survey_values(lines, levels_to_use, 7)

                #If levels to use is None than it's a survey type we don't care about
                if levels_to_use is not None:

                    #needed_for_completion is for when level 15 exists
                    needed_for_completion = [check_15, check_30, check_50, check_70]
                    #needed_for_completion_alt is for when level doesn't exist
                    needed_for_completion_alt = [check_50, check_70]

                    all_survey_levels = [check_15, check_20, check_30, check_50, check_60, check_70, check_80,
                                         check_90]
                    level_20_levels = [check_20, check_30, check_50, check_60, check_70, check_80, check_90]
                    level_60_levels = [check_60, check_70, check_80, check_90]
                    level_80_levels = [check_80, check_90]
                    level_90_levels = [check_90]

                    if level_type == "15":
                        #level 15 exists
                        if survey_finish.lower() == "true" and survey_type not in self.who_cares:
                            #survey was finished and the survey type is relevant

                            if self.check_for_real_survey_finish(needed_for_completion) is True:
                                #survey was finished and all required fields were finished as well
                                self.add_completion_value_to_dictionary(temp_count_dict, survey_type)
                                self.count_survey_levels(all_survey_levels, levels_to_use, survey_type, temp_count_dict)
                                self.optional_level_counter(level_20_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 1, survey_finish)
                                self.optional_level_counter(level_60_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 4, survey_finish)
                                self.optional_level_counter(level_80_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 6, survey_finish)
                                self.optional_level_counter(level_90_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 7, survey_finish)

                            else:
                                #survey was finished but not all the required fields. Adding counts for the fields
                                #but not for survey complete
                                self.count_survey_levels(all_survey_levels, levels_to_use, survey_type, temp_count_dict)
                                self.optional_level_counter(level_20_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 1, survey_finish)
                                self.optional_level_counter(level_60_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 4, survey_finish)
                                self.optional_level_counter(level_80_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 6, survey_finish)
                                self.optional_level_counter(level_90_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 7, survey_finish)

                        elif survey_finish.lower() != "true" and survey_type not in self.who_cares:
                            #survey was not finished so just adding counts for the fields
                            self.count_survey_levels(all_survey_levels, levels_to_use, survey_type, temp_count_dict)
                            self.optional_level_counter(level_20_levels, levels_to_use, survey_type,
                                                        temp_level_count_dict, 1, survey_finish)
                            self.optional_level_counter(level_60_levels, levels_to_use, survey_type,
                                                        temp_level_count_dict, 4, survey_finish)
                            self.optional_level_counter(level_80_levels, levels_to_use, survey_type,
                                                        temp_level_count_dict, 6, survey_finish)
                            self.optional_level_counter(level_90_levels, levels_to_use, survey_type,
                                                        temp_level_count_dict, 7, survey_finish)

                    elif level_type == "40":
                        #level 15 does not exist (older surveys before the change)
                        if survey_finish.lower() == "true" and survey_type not in self.who_cares:
                            #survey was finished and the survey type is relevant

                            if self.check_for_real_survey_finish(needed_for_completion_alt) is True:
                                #survey was finished and all required fields were finished as well
                                self.add_completion_value_to_dictionary(temp_count_dict, survey_type)
                                self.count_survey_levels(all_survey_levels, levels_to_use, survey_type, temp_count_dict)
                                self.optional_level_counter(level_20_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 1, survey_finish)
                                self.optional_level_counter(level_60_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 4, survey_finish)
                                self.optional_level_counter(level_80_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 6, survey_finish)
                                self.optional_level_counter(level_90_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 7, survey_finish)

                            else:
                                #survey was finished but not all the required fields. Adding counts for the fields
                                #but not for survey complete
                                self.count_survey_levels(all_survey_levels, levels_to_use, survey_type, temp_count_dict)
                                self.optional_level_counter(level_20_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 1, survey_finish)
                                self.optional_level_counter(level_60_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 4, survey_finish)
                                self.optional_level_counter(level_80_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 6, survey_finish)
                                self.optional_level_counter(level_90_levels, levels_to_use, survey_type,
                                                            temp_level_count_dict, 7, survey_finish)

                        elif survey_finish.lower() != "true" and survey_type not in self.who_cares:
                            #survey was not finished so just adding counts for the fields
                            self.count_survey_levels(all_survey_levels, levels_to_use, survey_type, temp_count_dict)
                            self.optional_level_counter(level_20_levels, levels_to_use, survey_type,
                                                        temp_level_count_dict, 1, survey_finish)
                            self.optional_level_counter(level_60_levels, levels_to_use, survey_type,
                                                        temp_level_count_dict, 4, survey_finish)
                            self.optional_level_counter(level_80_levels, levels_to_use, survey_type,
                                                        temp_level_count_dict, 6, survey_finish)
                            self.optional_level_counter(level_90_levels, levels_to_use, survey_type,
                                                        temp_level_count_dict, 7, survey_finish)
                else:
                    continue

            #Send the data to the sql database then reset the header list and the temp count dict
            db = dbq()
            db.data_to_database(temp_count_dict, use_date)
            db.data_to_level_tables_in_database(temp_level_count_dict, use_date)
            self.update_progress.emit(current_file_number + 1)
            time.sleep(.1)
            self.names = None
            #print temp_count_dict
            temp_count_dict = {}
            temp_level_count_dict = {}

        ReadLogFiles.relevant_files = []
        self.update_string_progress.emit("All log files are currently up to date \n")
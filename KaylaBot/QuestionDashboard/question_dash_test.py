from KaylaBot.QuestionDashboard import question_database as db
import AnalysisTool.extract_data_xml as extract
import gui_code_behind as cb
import os

output_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\output_files\\"


# xml.ExtractXMLData("Kayla Question Activation Counts_1.xml").fix_xml_encoding(output_path)
# test = xml.ExtractXMLData(output_path + "Kayla Question Activation Counts_1.xml").row_name_entry_handler(header=True)
#
# print test.count_dictionary
# print test.title_header

#db.QuestionDashboardData().insert_numerator_dictionary_to_database(test.count_dictionary, "07-01-2014", test.title_header)

db.CreateDataBase()

#db.QuestionDashboardData().check_for_data()

#db.QuestionDashboardData().test_alt()

#test = li.CSVLogIterator(datetime.datetime(2014,9,1), datetime.datetime(2014,9,5))

#test.find_all_logs_survey()

#for row in test.iterate_files_return_row():
#    if test.new_file is True:
#        print "Whoop"
#    else:
#        continue

# for row in db.QuestionDashboardData().pull_all_numerator_data('Certifications_Certifications', '201407'):
#    print row

# numerator_dict = {}
# check_list = []
#
#
# def change_dict_values():
#
#     for question in cb.QuestionDashSupport().get_all_the_questions():
#         question = question.replace("/", "_").replace(" ", "_").replace("-", "_")
#         check_list.append(question)
#         numerator_dict[question] = {}
#
#
# def change_handler_values(handler):
#     for key_value in xml_handler.count_dictionary:
#
#         question = handler.title_header.replace("/", "_").replace(" ", "_").replace("-", "_")
#         onet = key_value[key_value.find("/PayScale Code ") + len("/PayScale Code "):].strip()
#         target_count = handler.count_dictionary[key_value]
#         numerator_dict[question][onet] = target_count
#
# all_files = os.listdir(output_path)
#
# change_dict_values()
# for files in all_files:
#     if '.zip' not in files:
#
#         xml_handler = extract.ExtractXMLData(output_path + files).row_name_entry_handler(header=True)
#         change_handler_values(xml_handler)
#
# for key in numerator_dict:
#     print key
#     print numerator_dict[key]
#     break
import data_extract_thread as analysis
import DateFunctions.datetimes_in as dates
import csv
import gui_code_behind as cb
import question_database as db
import Constants.constant_strings as c
import os

data_pull_thread = analysis.ExtractDataThread()
start_date = dates.DateTimeFormats().find_first_of_last_month()
current_month = dates.DateTimeFormats().return_last_month_as_y_m("-")


out_file_path = c.Constants().question_dashboard + current_month + "\\"

if not os.path.exists(out_file_path):
    os.makedirs(out_file_path)

if not data_pull_thread.isRunning():
    data_pull_thread.get_date_non_gui(start_date)
    data_pull_thread.start()

def write_data_to_file():

    file_name = "Question_Dashboard.csv"

    update_line = "Writing to file at %s" % out_file_path
    print update_line
    with open(out_file_path + file_name, 'wb') as W:
        writer = csv.writer(W, lineterminator='\n')

        write_overall_to_file(writer)

    print "File writing complete."


def write_overall_to_file(writer):

    header = ['Date', 'Question', 'Active Profiles', 'Bailed 20', 'Saw 20', 'Saw MyPayScale',
              'Total Counts']
    writer.writerow(header)

    overall_dictionary = {}

    for question in cb.QuestionDashSupport().get_all_the_questions():

        data = db.QuestionDashboardData().pull_all_non_breadth_data(question, start_date.strftime("%Y%m"))
        overall_dictionary[question] = {'Active Profile': 0, 'Bailed 20': 0, 'Saw 20': 0, 'Saw MyPayScale': 0,
                                        'Total Counts': 0}
        date = None
        first = True
        for row in data:
            if first is True:
                date = row[0]
                overall_dictionary[question]['Active Profile'] += row[2]
                overall_dictionary[question]['Bailed 20'] += row[3]
                overall_dictionary[question]['Saw 20'] += row[4]
                overall_dictionary[question]['Saw MyPayScale'] += row[5]
                overall_dictionary[question]['Total Counts'] += row[6]
                first = False
            else:
                overall_dictionary[question]['Active Profile'] += row[2]
                overall_dictionary[question]['Bailed 20'] += row[3]
                overall_dictionary[question]['Saw 20'] += row[4]
                overall_dictionary[question]['Saw MyPayScale'] += row[5]
                overall_dictionary[question]['Total Counts'] += row[6]

        current = overall_dictionary[question]
        final = date, question, current['Active Profile'], current['Bailed 20'], current['Saw 20'], \
            current['Saw MyPayScale'], current['Total Counts']
        writer.writerow(final)

write_data_to_file()
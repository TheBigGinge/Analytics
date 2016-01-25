import sys
from Constants import constant_strings as c
sys.path.append(c.Constants().payscale_analytics)
from Constants import constant_strings as c
import AnalyticsTools.ConversionMetricsGUI.gui_interface as gui
import AnalyticsTools.ConversionMetricsGUI.file_cycle as file_cycle
import AnalyticsTools.ConversionMetricsGUI.database as database
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


"""
This script checks the last two weeks of level conversion with the two weeks previous to those
It then emails a file of all the tests to the data team.
"""


def database_check():
    if gui.UIForm.current_date_check():
        print "Database is up to date \n"
    else:
        print "Updating database \n"
        all_consumer_logs = os.listdir(c.Constants().log_path)
        log_files_already_used = database.DataBaseQueries.pull_all_used_dates()
        file_cycle.ReadLogFiles(all_consumer_logs, log_files_already_used).run()


def date_string(current_time):
    """
    Changing datetime to strings that work with the
    the conversion database
    """

    year = str(current_time.year)
    month = str(current_time.month)
    day = str(current_time.day)

    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day

    return year + month + day


def create_date_prior_date(start_time, days_ago):

    two_weeks_ago = start_time-datetime.timedelta(days=days_ago)

    return two_weeks_ago


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


def pull_data(start_time, end_time, surveys):

    dictionary_list = []
    final_counts = {}

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
    conversion_90 = database.DataBaseQueries().pull_conversions_for_optional_levels("level_90",
                                                                                    surveys,
                                                                                    start_time, end_time)
    dictionary_list.append(conversion)
    dictionary_list.append(conversion_20)
    dictionary_list.append(conversion_60)
    dictionary_list.append(conversion_80)
    dictionary_list.append(conversion_90)

    for i, dictionaries in enumerate(dictionary_list):
        if i == 0:

            final_counts = dictionaries

        else:

            final_counts = count_dictionaries(final_counts, dictionaries)

    return final_counts


def auto_email_alert():
    file_list = ["FastTrack_", "FastTrack-Edit_",
                 "JobOffer_"]
    #FROM = "DataAlerts@payscale.com"
    FROM = "Data Alerts@payscale.com"
    TO = ["Data Team@payscale.com"]

    msg = MIMEMultipart()
    msg['Subject'] = "Conversion Level Alert"
    msg['To'] = 'Data Team@payscale.com'

    body = ""
    alert_path = c.Constants().consumer_alert_files
    main_message = "The weekly conversion level tests have finished. You can find them at %s, %s, and %s" % \
                   (os.path.normpath(alert_path + file_list[0] + today + "_Conversion_Alert_Comparison.csv"),
                    os.path.normpath(alert_path + file_list[1] + today + "_Conversion_Alert_Comparison.csv"),
                    os.path.normpath(alert_path + file_list[2] + today + "_Conversion_Alert_Comparison.csv"))

    msg.attach(MIMEText(main_message))

    server = smtplib.SMTP('owa.payscale.com')
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()

if __name__ == '__main__':
    database_check()
    today = date_string(datetime.datetime.now())

    '''Building both two week periods below'''
    current_day = datetime.datetime.now()
    yesterday = create_date_prior_date(current_day, 1)

    first_period_begin = create_date_prior_date(yesterday, 14)

    second_period_end = create_date_prior_date(first_period_begin, 1)
    second_period_begin = create_date_prior_date(second_period_end, 14)

    yesterday = date_string(yesterday)
    first_period_begin = date_string(first_period_begin)
    second_period_end = date_string(second_period_end)
    second_period_begin = date_string(second_period_begin)

    '''Creating the count dictionaries'''
    fast_track_now = pull_data(first_period_begin, yesterday, "FastTrack")
    fast_track_then = pull_data(second_period_begin, second_period_end, "FastTrack")

    fast_edit_now = pull_data(first_period_begin, yesterday, "FastTrack_Edit")
    fast_edit_then = pull_data(second_period_begin, second_period_end, "FastTrack_Edit")

    job_offer_now = pull_data(first_period_begin, yesterday, "JobOffer")
    job_offer_then = pull_data(second_period_begin, second_period_end, "JobOffer")

    '''Creating the csv files that hold the analysis'''
    gui.UIForm().compare_data_to_csv("JobOffer", job_offer_now, job_offer_then, first_period_begin,
                                     yesterday, second_period_begin, second_period_end, today)

    gui.UIForm().compare_data_to_csv("FastTrack", fast_track_now, fast_track_then, first_period_begin,
                                     yesterday, second_period_begin, second_period_end, today)

    gui.UIForm().compare_data_to_csv("FastTrack-Edit", fast_edit_now, fast_edit_then, first_period_begin,
                                     yesterday, second_period_begin, second_period_end, today)
    auto_email_alert()
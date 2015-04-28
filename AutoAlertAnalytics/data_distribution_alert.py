import sys
sys.path.append("C:\\hg\\payscale\\users\\ryanm\\PayScaleAnalytics\\")
import datetime
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import DataDistributions.data_dist_database as db
import DateFunctions.date_functions as df
import DataDistributions.data_distributions as dd


alert_writing_path = '\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\Distributions_Alert_Report\\'
today = datetime.datetime.today()
string_today = df.DateFunctions().datetime_to_string_y_m_d(today, "-")

print "Running weekly queries..."
dd.DataDistributions().run_weekly_analysis_tool_queries()
dd.DataDistributions().update_weekly_database()

if today.day < 9:
    print "Running monthly queries..."
    dd.DataDistributions().run_monthly_analysis_tool_queries()
    dd.DataDistributions().update_monthly_database()

monthly_reports = ['onet_forty',
                   'onet_forty_overall',
                   'naics_codes',
                   'naics_codes_overall',
                   'metro_main',
                   'metro_main_overall',
                   'degree_affinities',
                   'degree_affinities_overall',
                   'company_size',
                   'company_size_overall',
                   'age_ranges',
                   'age_ranges_overall',
                   'years_experience',
                   'years_experience_overall',
                   'rollups',
                   'rollups_overall']

six_months_ago, this_month = dd.DataDistributions().find_monthly_date_values()
last_sunday, six_weeks_prior = dd.DataDistributions().find_weekly_date_values()

print "Pulling data..."
actives = list(set(db.DatabaseWork().pull_weekly_values('active_profiles', last_sunday, six_weeks_prior)))
total_profiles = list(set(db.DatabaseWork().pull_weekly_values('overall_profiles', last_sunday, six_weeks_prior)))

onet = sorted(db.DatabaseWork().pull_monthly_values('onet_forty', this_month, six_months_ago), reverse=True)
onet_overall = sorted(db.DatabaseWork().pull_monthly_values('onet_forty_overall', this_month, six_months_ago),
                      reverse=True)

naics = sorted(db.DatabaseWork().pull_monthly_values('naics_codes', this_month, six_months_ago), reverse=True)
naics_overall = sorted(db.DatabaseWork().pull_monthly_values('naics_codes_overall', this_month, six_months_ago),
                       reverse=True)
metro = sorted(db.DatabaseWork().pull_monthly_values('metro_main', this_month, six_months_ago), reverse=True)
metro_overall = sorted(db.DatabaseWork().pull_monthly_values('metro_main_overall', this_month, six_months_ago),
                       reverse=True)
degree = sorted(db.DatabaseWork().pull_monthly_values('degree_affinities', this_month, six_months_ago), reverse=True)
degree_overall = sorted(db.DatabaseWork().pull_monthly_values('degree_affinities_overall', this_month, six_months_ago),
                        reverse=True)
company = sorted(db.DatabaseWork().pull_monthly_values('company_size', this_month, six_months_ago, employer_size=True),
                 reverse=True)
company_overall = sorted(db.DatabaseWork().pull_monthly_values('company_size_overall', this_month, six_months_ago,
                                                               employer_size=True), reverse=True)
age = sorted(db.DatabaseWork().pull_monthly_values('age_ranges', this_month, six_months_ago), reverse=True)
age_overall = sorted(db.DatabaseWork().pull_monthly_values('age_ranges_overall', this_month, six_months_ago),
                     reverse=True)
years = sorted(db.DatabaseWork().pull_monthly_values('years_experience', this_month, six_months_ago), reverse=True)
years_overall = sorted(db.DatabaseWork().pull_monthly_values('years_experience_overall', this_month, six_months_ago),
                       reverse=True)
rollups = sorted(db.DatabaseWork().pull_monthly_values('rollups', this_month, six_months_ago), reverse=True)
rollups_overall = sorted(db.DatabaseWork().pull_monthly_values('rollups_overall', this_month, six_months_ago),
                         reverse=True)


print "Writing Active Profile Analysis to file..."
with open(alert_writing_path + "_Weekly_Data_Distributions_Alert.csv", 'a') as W:
    writer = csv.writer(W, lineterminator='\n')

    #header = ['Date', 'Current Week Active Count', 'Current Week Total Count', 'Percentage',
    #          'Past Month Active Count', 'Past Month Total Count', 'Percentage', 'Chi Square Statistic', 'P-Value',
    #          'Difference in Activation']

    #writer.writerow(header)

    writer.writerow(dd.DataDistributions().create_weekly_statistics(actives, total_profiles))

if today.day < 9:
    with open(alert_writing_path + string_today + "_Monthly_Data_Distributions_Alert.csv", 'wb') as W:
        writer = csv.writer(W, lineterminator='\n')

        header = ['Category', 'Category Type', 'Current Month Active Count', 'Current Month Total Count', 'Percentage',
                  'Past 4 Months Active Count', 'Past 4 Months Total Count', 'Percentage', 'Chi Square Statistic',
                  'P-Value', 'Difference in Activation']

        writer.writerow(header)

        print "Writing ONET profile statistics to file..."
        for items in dd.DataDistributions().create_monthly_statistics(onet, onet_overall, 'ONET'):
            if items[9] < .05:
                if items[4] < 1 and items[7] < 1 and items[2] > 5:
                    writer.writerow(items)

        print "Writing NAICS profile statistics to file..."
        for items in dd.DataDistributions().create_monthly_statistics(naics, naics_overall, 'NAICS'):
            if items[9] < .05:
                if items[4] < 1 and items[7] < 1 and items[2] > 5:
                    writer.writerow(items)

        print "Writing METRO profile statistics to file..."
        for items in dd.DataDistributions().create_monthly_statistics(metro, metro_overall, 'METRO'):
            try:
                if items[9] < .05:
                    if items[4] < 1 and items[7] < 1 and items[2] > 5:
                        writer.writerow(items)
            except UnicodeEncodeError:
                pass

        print "Writing DEGREE profile statistics to file..."
        for items in dd.DataDistributions().create_monthly_statistics(degree, degree_overall, 'DEGREE'):
            if items[9] < .05:
                if items[4] < 1 and items[7] < 1 and items[2] > 5:
                    writer.writerow(items)

        print "Writing COMPANY SIZE profile statistics to file..."
        for items in dd.DataDistributions().create_monthly_statistics(company, company_overall, 'COMPANY SIZE'):
            if items[9] < .05:
                if items[4] < 1 and items[7] < 1 and items[2] > 5:
                    writer.writerow(items)

        print "Writing AGE profile statistics to file..."
        for items in dd.DataDistributions().create_monthly_statistics(age, age_overall, 'AGE'):
            if items[9] < .05:
                if items[4] < 1 and items[7] < 1 and items[2] > 5:
                    writer.writerow(items)

        print "Writing YEARS EXPERIENCE profile statistics to file..."
        for items in dd.DataDistributions().create_monthly_statistics(years, years_overall, 'YEARS EXPERIENCE'):
            if items[9] < .05:
                if items[4] < 1 and items[7] < 1 and items[2] > 5:
                    writer.writerow(items)

        print "Writing ROLLUPS profile statistics to file..."
        for items in dd.DataDistributions().create_monthly_statistics(rollups, rollups_overall, 'ROLLUPS'):
            if items[9] < .05:
                if items[4] < 1 and items[7] < 1 and items[2] > 5:
                    writer.writerow(items)


#FROM = "DataAlerts@payscale.com"
FROM = "Data Alerts@payscale.com"
TO = ["Data Team@payscale.com"]

attachment = 'C:\\users\\ryanm\\desktop\\JL.jpg'

msg = MIMEMultipart()
msg['Subject'] = "Data Distributions Alerts"
msg['To'] = 'Data Team@payscale.com'

body = ""
if today.day < 6:
    main_message = "The Data Distribution Analysis has completed. You can find the results at %s and %s" % \
                   (os.path.normpath(alert_writing_path + "_Weekly_Data_Distributions_Alert.csv"),
                    os.path.normpath(alert_writing_path + string_today + "_Monthly_Data_Distributions_Alert.csv"))
else:
    main_message = "The Data Distribution Analysis has completed. You can find the results at %s " % \
                   (os.path.normpath(alert_writing_path + "_Weekly_Data_Distributions_Alert.csv"))

msgText = MIMEText('<b>%s</b><br><img src="cid:C:\\users\\ryanm\\desktop\\JL.jpg"><br>' % body, 'html')

msg.attach(MIMEText(main_message))
#msg.attach(msgText)

server = smtplib.SMTP('owa.payscale.com')
server.sendmail(FROM, TO, msg.as_string())
server.quit()

print "!!!Data Distribution Alerts Completed!!!"
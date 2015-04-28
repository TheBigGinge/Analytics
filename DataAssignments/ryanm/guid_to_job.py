import LogFileTools.log_iterator as log
import datetime
import csv

survey_path = '\\\\psfiler01\\data\\SurveyReports\\'
iterator = log.CSVLogIterator(datetime.datetime(2014, 5, 1), datetime.datetime(2014, 9, 30))
iterator.find_all_logs_survey()

needed_guid = set()
with open("C:\\users\\ryanm\\desktop\\GUIDs.csv", 'rb') as R:
    reader = csv.reader(R, delimiter=',')

    for row in reader:
        match_guid = row[0]
        needed_guid.add(match_guid)

results = []
for log_files in iterator.log_files_to_use:

    try:
        print "Working on " + log_files
        with open(survey_path + log_files, 'rb') as R:
            reader = csv.reader(R, delimiter=',')

            header = reader.next()
            for row in reader:
                guid = row[header.index("ProfileGuid")]
                job_title = row[header.index("Profile job")]

                if guid in needed_guid:
                    final = guid, job_title
                    results.append(final)
    except IOError:
        continue

print "Writing to file..."
with open("C:\\users\\ryanm\\desktop\\Disabled Results.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    for row in results:
        writer.writerow(row)
import os
import datetime
import csv
import collections

data_path = '\\\\filer01\\public\\Data_Analytics\\Consumer Log Metrics\\Data Files\\'
log_path_write = '\\\\psfiler01\\data\\SurveyReports\\old\\'
log_path = '\\\\psfiler01\\data\\SurveyReports\\'
data_path_alt = '\\\\filer01\\public\\Data_Analytics\\Consumer Log Metrics\\'
histogram_path = '\\\\filer01\\public\\Data_Analytics\\Consumer Log Metrics\\Histogram Data\\'


class NewLogFiles:

    log_files = os.listdir('\\\\psfiler01\\data\\SurveyReports')
    todays_date = ""
    log_files_to_use = []

    def __init__(self):
        self.fancy = 'fancy'
        self.current_date()
        self.proper_files()

    @staticmethod
    def current_date():
        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month)
        if len(month) == 1:
            month = "0" + str(month)
        else:
            month = str(month)

        final_date = year + month
        NewLogFiles.todays_date += final_date

    @staticmethod
    def proper_files():
        #Filter out the log files that I don't need and append the ones I do need to the LogFilesList
        previous_files = os.listdir(data_path)
        previous_dates = set()

        for files in previous_files:
            date_check = files[0:6]
            previous_dates.add(date_check)

        for files in NewLogFiles.log_files:
            if "aggregate" in files:
                continue
            elif ".csv" not in files:
                continue
            elif "201204" in files or "201205" in files:
                continue
            elif "old" in files:
                continue
            elif NewLogFiles.todays_date in files:
                continue
            elif files[18:24] in previous_dates:
                continue
            else:
                NewLogFiles.log_files_to_use.append(files)


class LogDataPull:

    def __init__(self, new_log_files, job_set):
        self.new_log_files = new_log_files
        self.job_set = job_set
        self.cycle_through_logs(self.new_log_files)

    def cycle_through_logs(self, new_log_files):

        for i, files in enumerate(self.new_log_files):
            print "Working on " + new_log_files[i]
            with open(log_path + new_log_files[i]) as R:
                log_file = csv.reader(R, delimiter=',')
                names = log_file.next()

                if "Profile job" in names:
                    for row in log_file:

                        if i % 5000 == 0 and i != 0:
                            print "Processed %s rows..." % i

                        if "JobOffer" in row or "CurrentJob" in row:

                            #survey_type = row[names.index("SurveyType")]
                            passed_data = row[names.index('PassedInData')]
                            profile_job = row[names.index('Profile job')]
                            activated = row[names.index('Activated')]
                            unprompted = row[names.index('Job\Job Unprompted')]
                            browse = row[names.index('BrowseConfirm10')]
                            saw = row[names.index('Saw20')]
                            #Change Completed Survey to SawMyPayScale due to log header errors
                            complete = row[names.index('SawMyPayscale')]
                            unprompted_2 = row[names.index('Profile job.unprompted')]

                            #final_job = self.job_creator(profile_job, unprompted)
                            hist_job = self.hist_job_creator(unprompted, unprompted_2, profile_job)

                            CountInstances(self.job_set, profile_job, passed_data, activated, browse, saw, complete,
                                           hist_job)

                    if i + 1 > len(new_log_files) - 1:

                        unique_count = len(CountInstances.unique_unc_string_count)
                        CountInstances.count_dictionary["Unique UNC Strings"] = unique_count
                        self.write_to_file(new_log_files[i])

                    elif new_log_files[i][18:24] != new_log_files[i + 1][18:24]:

                        unique_count = len(CountInstances.unique_unc_string_count)
                        CountInstances.count_dictionary["Unique UNC Strings"] = unique_count
                        self.write_to_file(new_log_files[i])

                    else:
                        continue

    @staticmethod
    def write_to_file(log_file):

        date = log_file[18:24]
        year = int(date[:4])
        month = int(date[4:6])
        in_file_date = str(datetime.datetime(year, month, 1).strftime("%Y-%m"))

        with open(data_path + date + " Unconfirmed Strings.csv", 'w') as W:
            writer = csv.writer(W, lineterminator='\n')

            header = ["Date", "Type", "Counts"]
            writer.writerow(header)

            for keys in CountInstances.count_dictionary:
                final = in_file_date, keys, CountInstances.count_dictionary[keys]
                writer.writerow(final)

        with open(histogram_path + date + " Histogram Files.csv", 'w') as W:
            writer = csv.writer(W, lineterminator='\n')

            header = ["String", "Counts"]
            writer.writerow(header)

            histogram_dictionary = collections.Counter(CountInstances.histogram_list)

            for keys in histogram_dictionary:
                if keys == "":
                    continue
                else:
                    final = keys, histogram_dictionary[keys]

                    writer.writerow(final)

        CountInstances.count_dictionary = {}
        CountInstances.unique_unc_string_count = set()
        CountInstances.histogram_list = []

    @staticmethod
    def job_creator(profile_job, unprompted):
        if profile_job == '':
            final = unprompted
        else:
            final = profile_job
        return final

    @staticmethod
    def hist_job_creator(unprompted, unprompted_2, profile_job):
        if unprompted == '' and unprompted_2 == '':
            final = profile_job
        if unprompted == '' and unprompted_2 != '':
            final = unprompted_2
        if unprompted != '':
            final = unprompted
        return final


class CountInstances:

    count_dictionary = {}
    unique_unc_string_count = set()
    histogram_list = []

    def __init__(self, job_set, profile_job, passed_data, activated, browse, saw, complete, hist_job):
        self.job_set = job_set
        self.profile_job = profile_job
        self.passed_data = passed_data
        self.activated = activated
        self.browse = browse
        self.saw = saw
        self.complete = complete
        self.hist_job = hist_job
        CountInstances.histogram_list.append(self.hist_job)

        self.all_counter(self.profile_job, self.passed_data)
        self.all_survey_completes(self.profile_job, self.complete)
        self.active(self.activated)
        self.browse_true(self.browse)
        self.unconfirmed_string_counter(self.profile_job, self.passed_data, self.job_set)
        self.unprompted_counter(self.profile_job, self.job_set)
        self.browse_true_saw_fail(self.browse, self.saw)
        self.confirm_complete(self.profile_job, self.complete, self.job_set)
        self.confirm_no_complete(self.profile_job, self.complete, self.job_set)
        self.unc_no_complete(self.profile_job, self.complete, self.job_set)
        self.unc_complete(self.profile_job, self.complete, self.job_set)
        self.overall_count(self.profile_job, self.job_set)
        self.unique_unc_strings(self.profile_job, self.passed_data, self.job_set)

    @staticmethod
    def all_counter(profile_job, passed_data):
        #Profile Job doesn't equal "" and Data Passed In (number of searches with data entered)
        if profile_job != "" and passed_data == 'true':
            try:
                CountInstances.count_dictionary["All Data"] += 1
            except KeyError:
                CountInstances.count_dictionary["All Data"] = 1

    @staticmethod
    def all_survey_completes(profile_job, complete):
        #Job isn't blank and Survey Complete is True
        if profile_job != "" and complete == 'True':
            try:
                CountInstances.count_dictionary["All Survey Completes"] += 1
            except KeyError:
                CountInstances.count_dictionary["All Survey Completes"] = 1

    @staticmethod
    def active(actives):
        #Activated is True in the Consumer Log Reports
        if actives != '':
            try:
                CountInstances.count_dictionary["All Activateds"] += 1
            except KeyError:
                CountInstances.count_dictionary["All Activateds"] = 1

    @staticmethod
    def browse_true(browse):
        #Browse and Confirm True only
        if browse == 'True':
            try:
                CountInstances.count_dictionary["Browse True"] += 1
            except KeyError:
                CountInstances.count_dictionary["Browse True"] = 1

    @staticmethod
    def unconfirmed_string_counter(profile_job, passed_data, job_set):
        #Profile Job not CFM'd, doesn't = "" and data passed in
        if profile_job not in job_set and profile_job != "" and passed_data != "":
            try:
                CountInstances.count_dictionary["Unc"] += 1
            except KeyError:
                CountInstances.count_dictionary["Unc"] = 1

    @staticmethod
    def unprompted_counter(profile_job, job_set):
        #Profile Job doesn't equal "" and is not confirmed
        if profile_job != "" and profile_job not in job_set:
            try:
                CountInstances.count_dictionary["Entries"] += 1
            except KeyError:
                CountInstances.count_dictionary["Entries"] = 1

    @staticmethod
    def browse_true_saw_fail(browse, saw):
        #Browse and Confirm True and Saw20 False
        if browse == 'True' and saw == 'False':
            try:
                CountInstances.count_dictionary["Browse"] += 1
            except KeyError:
                CountInstances.count_dictionary["Browse"] = 1

    @staticmethod
    def confirm_complete(profile_job, complete, job_set):
        #Chose a confirmed job and completed the survey
        if profile_job in job_set and profile_job != "" and complete == 'True':
            try:
                CountInstances.count_dictionary["ConfComplete"] += 1
            except KeyError:
                CountInstances.count_dictionary["ConfComplete"] = 1

    @staticmethod
    def confirm_no_complete(profile_job, complete, job_set):
        #Chose a confirmed job and did not complete the survey
        if profile_job in job_set and complete == 'False':
            try:
                CountInstances.count_dictionary["ConfNoComplete"] += 1
            except KeyError:
                CountInstances.count_dictionary["ConfNoComplete"] = 1

    @staticmethod
    def unc_no_complete(profile_job, complete, job_set):
        #Jobs is not confirmed not blank and survey complete is true
        if profile_job not in job_set and profile_job != "" and complete == 'False':
            try:
                CountInstances.count_dictionary["UncNoComplete"] += 1
            except KeyError:
                CountInstances.count_dictionary["UncNoComplete"] = 1

    @staticmethod
    def unc_complete(profile_job, complete, job_set):
        #Jobs is not confirmed not blank and survey complete is false
        if profile_job not in job_set and profile_job != "" and complete == 'True':
            try:
                CountInstances.count_dictionary["UncComplete"] += 1
            except KeyError:
                CountInstances.count_dictionary["UncComplete"] = 1

    @staticmethod
    def overall_count(profile_job, job_set):
        #Every Entry in the log
        if profile_job != "":
            try:
                CountInstances.count_dictionary["Overall Count"] += 1
            except KeyError:
                CountInstances.count_dictionary["Overall Count"] = 1

    @staticmethod
    def unique_unc_strings(profile_job, passed_data, job_set):
        #Job is not empty, not confirmed and Data Passed In
        if profile_job != "" and profile_job not in job_set and passed_data != "":
            CountInstances.unique_unc_string_count.add(profile_job)
import FileHandling.file_work as fw
import Statistics.entropy as entropy
import DateFunctions.datetimes_in as di
import csv
import getpass
import os
import numpy as np

unprompted_path = "\\\\filer01\\public\\Data_Analytics\\Job Rollup Suggesting\\Unprompted Strings Files\\"
job_suggestion_path = "\\\\filer01\\public\\Data_Analytics\\Job Rollup Suggesting\\Job Rollup Suggestions\\"
local_path = os.path.expanduser("~"+getpass.getuser())+"\\desktop\\"
final_suggestions = "\\\\filer01\\public\\Data_Analytics\\Job Rollup Suggesting\\Final Suggestions\\"

#current_job_suggestions = di.DateTimeFormats().find_first_of_current_month().strftime("%Y%m") +\
#    ' Jobs Without Rollups Suggestions.csv'


def current_rollup_suggestions():
    file_dict = {}
    newest_time = None

    suggestion_file = None

    for files in os.listdir(job_suggestion_path):
        mtime = os.stat(job_suggestion_path + files).st_mtime
        file_dict[files] = mtime
        items = file_dict.values()
        newest_time = max(items)

    for keys in file_dict:
        if file_dict[keys] == newest_time:
            suggestion_file = keys

    return suggestion_file


class SuggestRollups:
    
    def __init__(self, unprompted_files, eac_dict, jobs_without_rollups):
        self.jobs_without_rollups = jobs_without_rollups
        self.job_eac_dict = eac_dict
        self.unprompted_files = os.listdir(unprompted_path)
        self.current_unprompted = self.find_current_unprompted_strings()
        match_list = self.unprompted_pull()
        similar_jobs = self.match_rollups(match_list)
        print "Moving to the Writing"
        self.write_matches(similar_jobs)

    def find_current_unprompted_strings(self):
        file_dict = {}
        newest_time = None

        for files in self.unprompted_files:
            mtime = os.stat(unprompted_path + files).st_mtime
            file_dict[files] = mtime
            items = file_dict.values()
            newest_time = max(items)

        for keys in file_dict:
            if file_dict[keys] == newest_time:
                return keys

    def unprompted_pull(self):
        
        matching_list = []
        
        append = matching_list.append
        print "Sorting through the unprompted strings file"

        handler = fw.FileHandler()

        for row in handler.open_csv(unprompted_path + self.current_unprompted):
            unprompted = row[1]
            confirmed = row[0]
            mutual_information = row[5]
            word_similarity = row[6]

            all = unprompted, confirmed, mutual_information, word_similarity

            if float(mutual_information) > 12 and float(word_similarity) < .9:
                append(all)

            else:
                continue

        return matching_list

    def match_rollups(self, match_list):
        
        match = []
        append = match.append
        print "Matching Jobs within lists. Sit back and wait... this takes some time \n"
        for i, jobs in enumerate(self.jobs_without_rollups):

            print "Now working on job number %s" % (i + 1)
             
            similarity = map(lambda line: entropy.Entropy(jobs, line[0]).final, match_list)
            for item in similarity:
                if item > .9:
                    matches = match_list[similarity.index(item)][0], jobs, item
                    print matches
                    append(matches)

                else:
                    continue
        return match

    @staticmethod
    def write_matches(jobs_list):
        #TODO: Evaluate matches before writing them to file and then evaluating
        print "Writing suggestions to file"
        try:
            with open(job_suggestion_path + current_rollup_suggestions(), 'w') as f:
                writer = csv.writer(f, lineterminator='\n')
                for row in jobs_list:
                    writer.writerow(row)
        except IOError:
            with open(local_path + current_rollup_suggestions(), 'w') as f:
                writer = csv.writer(f, lineterminator='\n')
                for row in jobs_list:
                    writer.writerow(row)


class JobEACDifference:

    def __init__(self, job_eac_dict):
        self.unprompted_files = os.listdir(unprompted_path)
        self.job_eac_dict = job_eac_dict
        self.rollup_dict = {}
        self.create_rollup_dict()
        self.suggestions_list = []
        self.open_file()
        self.look_up = self.pull_and_order_unprompted()
        self.final_list = []
        self.analyze_jobs()

    def open_file(self):

        print "Opening Rollup Suggestions file \n"

        with open(job_suggestion_path + current_rollup_suggestions(), 'rb') as f:
            reader = csv.reader(f, delimiter=',')

            for row in reader:
                self.suggestions_list.append(row)

    def calculate_difference_error(self, first_job, second_job):
        try:
            first = self.job_eac_dict[first_job]
        except KeyError:
            try:
                first = self.job_eac_dict[self.rollup_dict[first_job]]
            except KeyError:
                return "N/A"
        try:
            second = self.job_eac_dict[second_job]
        except KeyError:
            return "N/A"

        error = np.sqrt((float(first[1]) * float(first[1])) / float(first[2]) + (float(second[1]) *
                                                                                 float(second[1])) / float(second[2]))

        return error

    def analyze_jobs(self):

        print "Analyzing Pay"

        for row in self.suggestions_list:

            first_job = self.look_up[row[0]]

            try:
                rollup = self.rollup_dict[first_job]
                first = self.job_eac_dict[rollup]
            except KeyError:
                rollup = 'None'

                try:
                    first = self.job_eac_dict[first_job]
                except KeyError:
                    first = 'N/A'

            second_job = row[1]
            mi = row[2]

            try:
                second = self.job_eac_dict[second_job]
            except KeyError:
                second = 'N/A'

            if first == 'N/A' or second == 'N/A':
                difference = 'N/A'
                diff_error = 'N/A'

            if first != 'N/A' and second != 'N/A':
                try:
                    difference = abs((float(first[0]) - float(second[0])) / float(second[0]))
                    diff_error = self.calculate_difference_error(first_job, second_job)
                except ValueError:
                    print first[0], second[0]

            rollup_key_check = self.rollup_dict.keys()

            if first_job in rollup_key_check:
                rollup = self.rollup_dict[first_job]

            try:
                examined_job_rollup = self.rollup_dict[second_job]
            except KeyError:
                examined_job_rollup = second_job

            if examined_job_rollup == rollup:
                continue

            if isinstance(first[0], float) is not True or isinstance(second[0], float) is not True:
                final = row[0], first_job, second_job, mi, rollup, examined_job_rollup, first[0], second[0]

            if isinstance(first[0], float) is True and isinstance(second[0], float) is True:
                final = row[0], first_job, second_job, mi, rollup, examined_job_rollup, round(float(first[0]), 2),\
                    round(float(second[0]), 2)

            if difference > .2 and difference > diff_error:
                continue

            elif .2 < difference <= diff_error:
                self.final_list.append(final)

            else:
                self.final_list.append(final)

        print "Writing to file"

        write_date = str(di.DateTimeFormats().return_today_as_y_m("-"))

        with open(final_suggestions + write_date + " Job Rollup Suggestions.csv", 'w') as f:
            writer = csv.writer(f, lineterminator='\n')

            header = ['Unprompted String', 'Matched Job', 'Job Being Evaluated', 'Mutual Information',
                      'Rollup for Matched Job', 'Rollup for Job Being Evaluated', 'Matched Job EAC',
                      'Job Being Evaluated EAC']

            writer.writerow(header)

            for row in self.final_list:

                final = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]

                writer.writerow(final)

    def current_unprompted(self):
        file_dict = {}
        newest_time = None

        unprompted_file = None

        for files in self.unprompted_files:
            mtime = os.stat(unprompted_path + files).st_mtime
            file_dict[files] = mtime
            items = file_dict.values()
            newest_time = max(items)

        for keys in file_dict:
            if file_dict[keys] == newest_time:
                unprompted_file = keys

        return unprompted_file

    def pull_and_order_unprompted(self):

        content_list = []
        with open(unprompted_path + self.current_unprompted(), 'rb') as f:
            reader = csv.reader(f, delimiter=',')

            for row in reader:
                if 'Job Chosen' not in row:
                    mutual = row[5]
                    confirmed = row[0]
                    unprompted = row[1]
                    if float(mutual) > 11:
                        final = float(mutual), confirmed, unprompted
                        content_list.append(final)

        content_list.sort(reverse=False)

        match_dict = {}

        print "Creating Lookup Dictionary \n"
        for row in content_list:
            confirmed = row[1]
            unprompted = row[2]
            match_dict[unprompted] = confirmed

        return match_dict

    def create_rollup_dict(self):

        print "Creating Rollup Dictionary \n"

        with open('\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\Current Rollups.csv',
                  'rb') as f:

            reader = csv.reader(f, delimiter=',')
            header = reader.next()

            for row in reader:

                rule = row[header.index('RULE VALUE')]
                av = row[header.index('Read-only Answervalue')]

                self.rollup_dict[rule] = av

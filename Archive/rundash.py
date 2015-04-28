import os
import csv
import zipfile
import datetime
import xml.sax

import RequestService.admin_requests as request_service
import AnalysisTool.deserialize_xml as my_xml


ReportPath = '\\\\psstats03\\reports\\Results\\'
working_directory = os.getcwd()

TestFiles = ['Ryan Data Dashboard Job Counts_0.XML', 'Ryan Data Dashboard Job Counts_1.XML',
             'Ryan Data Dashboard Job Rollup Counts_0.XML', 'Ryan Data Dashboard Job Rollup Counts_1.XML',
             'Ryan Data Dashboard Job Counts 2_0.XML', 'Ryan Data Dashboard Job Counts 2_1.XML',
             'Ryan Data Dashboard Job Rollup Counts 2_0.XML', 'Ryan Data Dashboard Job Rollup Counts 2_1.XML']
             
IQRFiles = ['Ryan Data Dashboard IQR US PayScale Main_0.XML', 'Ryan Data Dashboard IQR US PSP Job Rollups_0.XML']


ModelFiles = ['Ryan Data Dashboard Jobs with Model US_0.XML', 'Ryan Data Dashboard Jobs with Model Canada_0.XML']

UNCFiles = ['Ryan Data Dashboard List of Jobs not Deactivation Rules 4 year_0.XML',
            'Ryan Data Dashboard List of Jobs not Deactivation Rules 4 year_1.XML',
            'Ryan Data Dashboard List of Jobs not Deactivation Rules 2 year_0.XML',
            'Ryan Data Dashboard List of Jobs not Deactivation Rules 2 year_1.xMl']

             
WritingPath = '\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\'

psp_file_path = "\\\\filer01\\public\\Data Dashboards\\PSP Zip Reports\\"

now = str(datetime.datetime.now())
todays_date = now[:7]
current_year, current_month = todays_date.split("-")
todays_date = todays_date.replace('-', '')
todays_date_alt = now[:7]

request_service.PullAnyAffinityType(None, None, {'field': 'job', 'breadth': '10'}, "Current Job Rollups",
                                    "\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\")

request_service.PullAnyAffinityType(None, "Unclassified", {'field': 'job'}, "Current Unclassified",
                                    "\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\")

request_service.PullCurrentAnswerValues("job", 2,
                                        "\\\\filer01\\public\\Data Dashboards\\"
                                        "Automated Dashboard Files\\Current Jobs.tsv")


class DataStorage:

    job_count_dict = {}
    job_iqr_dict = {}
    job_model_dict = {}
    psp_reports = []
    unc_counts = {}


def current_breadth_thirty():
    breadth_thirty = []

    print "Building the Current Breadth 30 tab..."
    with open(WritingPath + "Current Unclassified.tsv", 'rb') as R:
        reader = csv.reader(R, delimiter="\t")

        names = reader.next()

        for row in reader:
            affinity_name = row[names.index('NAME')]
            job_job = row[names.index('RULE VALUE')]
            answer_value = ''
            soc_code = row[names.index('soc code')]

            if '0.00' in soc_code:
                classified = "No"
            else:
                classified = soc_code

            final = affinity_name, job_job, answer_value, soc_code, classified
            breadth_thirty.append(final)

    with open(WritingPath + "Current Job Rollups.tsv", 'rb') as R:
        reader = csv.reader(R, delimiter='\t')

        names = reader.next()

        for row in reader:
            affinity_name = row[names.index('NAME')]
            job_job = row[names.index('RULE VALUE')]
            answer_value = row[names.index('Read-only Answervalue')]
            soc_code = row[names.index('soc code')]

            if '0.00' in soc_code:
                classified = "No"
            else:
                classified = soc_code

            final = affinity_name, job_job, answer_value, soc_code, classified
            breadth_thirty.append(final)

    with open(WritingPath + "Current Breadth 30.csv", 'w') as W:
        writer = csv.writer(W, lineterminator='\n')

        header = ['Affinity Name', 'Job/Job AV', 'PSP AV (Breadth 10 Affinities)', 'SOC Code',
                  'Classified in Breadth 30?']

        writer.writerow(header)

        for line in breadth_thirty:
            writer.writerow(line)

current_breadth_thirty()


class JobCountXMLExtractor:
    
    def __init__(self):
        for files in TestFiles:
            print "Pulling data from " + files
            self.file = files
            self.job_count_dict = {}
            self.open_file(files)
            self.write_to_file(files)
    
    def open_file(self, files):

        with my_xml.report_handler(my_xml.OverallDataCount) as handler:
            with open(ReportPath + files, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            self.job_count_dict = handler.count_dictionary
                    
    def write_to_file(self, files):
        if '_0' in files:
            DataStorage.job_count_dict['United States 4 Year ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_count_dict

        if '_1' in files:
            DataStorage.job_count_dict['Canada 4 Year ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_count_dict

        if '2_0' in files:
            DataStorage.job_count_dict['United States 2 Year ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_count_dict

        if '2_1' in files:
            DataStorage.job_count_dict['Canada 2 Year ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_count_dict

JobCountXMLExtractor()


class JobIQRXmlExtractor:
    
    def __init__(self):
        for files in IQRFiles:
            print "Pulling data from " + files + ". These IQR files are HUGE so hold on for a bit. \n"
            self.file = files
            self.job_iqr_dict = {}
            self.open_file(files)
            self.write_to_file(files)
            
    def open_file(self, files):

        with my_xml.report_handler(my_xml.NameIQRContentHandler) as handler:
            with open(ReportPath + files, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            return handler.count_dictionary

    def write_to_file(self, files):
        if '_0' in files:
            DataStorage.job_iqr_dict['United States ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_iqr_dict

        if '_1' in files:
            DataStorage.job_iqr_dict['Canada ' + files[len('Ryan Data Dashboard '):len(files)-4]] = self.job_iqr_dict


JobIQRXmlExtractor()


class JobModelDataXMLExtractor:
    
    def __init__(self):
        for files in ModelFiles:
            print "Pulling data from " + files
            self.file = files
            self.job_model_dict = {}
            self.open_file(files)
            self.write_to_file(files)
            
    def open_file(self, files):

        with my_xml.report_handler(my_xml.NameModelCountContentHandler) as handler:
            with open(ReportPath + files, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            self.job_model_dict = handler.count_dictionary

    def write_to_file(self, files):
        if 'US' in files:
            DataStorage.job_model_dict['United States ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_model_dict

        if 'Canada' in files:
            DataStorage.job_model_dict['Canada ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_model_dict

JobModelDataXMLExtractor()


def ng_strings_pull():
    print "Pulling the NG Strings list \n"
    ng_path = 'C:\\hg\\payscale\\data\\AnswerSearch\\'
    ng_file = 'Job.nogood'
    ng_strings_list = []
    with open(ng_path + ng_file, 'rb') as f:
        for line in f:
            ng_string = line.strip('\r\n')
            ng_strings_list.append(ng_string)
    return ng_strings_list
    
job_no_good = ng_strings_pull()

 
def extract_rollups():
    print "Finding the Current Rollups List \n"
    rollup_dict = {}
    with open(WritingPath + 'Current Job Rollups.tsv', 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        names = reader.next()
        for row in reader:
            rule_value = row[names.index('RULE VALUE')]
            answer_value = row[names.index('Read-only Answervalue')]
            rollup_dict[rule_value] = answer_value
    return rollup_dict
    
rollup_mapping = extract_rollups()


def rollup_lookup_for_tasks():

    rollup_dict = {}

    with open(WritingPath + 'Current Job Rollups.tsv', 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        names = reader.next()
        rollup_dict["All"] = set()
        for row in reader:
            rule_value = row[names.index('RULE VALUE')]
            answer_value = row[names.index('Read-only Answervalue')]
            try:
                rollup_dict[answer_value].append(rule_value)
                rollup_dict["All"].add(rule_value)
            except KeyError:
                rollup_dict[answer_value] = []
                rollup_dict[answer_value].append(rule_value)
                rollup_dict["All"].add(rule_value)

    return rollup_dict

task_rollup_mapping = rollup_lookup_for_tasks()


def extract_confirmed_jobs():
    print 'Finding the Current list of confirmed Jobs \n'
    #TODO: Find out why the tsv version is messed up
    jobs_list = []
    with open(WritingPath + 'Current Jobs.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        names = reader.next()
        for row in reader:
            job = row[names.index('ANSWER VALUE')]
            jobs_list.append(job)
    return jobs_list
    
current_jobs_list = extract_confirmed_jobs()


def extract_current_tasks():
    print "Pulling Jobs with Current Tasks \n"
    task_set = set()
    with open(WritingPath + 'Current Tasks.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        names = reader.next()
        for row in reader:
            job = row[names.index('JOB')]
            task_set.add(job)

    return task_set

jobs_with_tasks = extract_current_tasks()


def current_breadth_thirty():
    print "Pulling Breadth 30 Rollups \n"
    onet_dict = {}
    with open(WritingPath + 'Current Breadth 30.csv','rb') as f:
        reader = csv.reader(f, delimiter=',')
        names = reader.next()
        for row in reader:
            job_job = row[names.index('Job/Job AV')]
            classification = row[names.index('SOC Code')]
            if classification == "" and job_job in onet_dict.keys():
                continue
            onet_dict[job_job] = classification
    return onet_dict
    
onet_breadth_thirty = current_breadth_thirty()
            

class CreateCFMTab:
    
    def __init__(self):
        self.current_jobs = current_jobs_list
        self.rollup_dict = rollup_mapping
        self.no_good_strings = job_no_good
        self.tasks = jobs_with_tasks
        self.breadth_30 = onet_breadth_thirty
        self.task_jobs = task_rollup_mapping
        self.two_year_canada_jobs = DataStorage.job_count_dict['Canada 2 Year Job Counts 2_1']
        self.four_year_canada_jobs = DataStorage.job_count_dict['Canada 4 Year Job Counts_1']
        self.two_year_us_jobs = DataStorage.job_count_dict['United States 2 Year Job Counts 2_0']
        self.four_year_us_jobs = DataStorage.job_count_dict['United States 4 Year Job Counts_0']
        self.two_year_us_rollups = DataStorage.job_count_dict['United States 2 Year Job Rollup Counts 2_0']
        self.four_year_us_rollups = DataStorage.job_count_dict['United States 4 Year Job Rollup Counts_0']
        self.two_year_ca_rollups = DataStorage.job_count_dict['Canada 2 Year Job Rollup Counts 2_1']
        self.four_year_ca_rollups = DataStorage.job_count_dict['Canada 4 Year Job Rollup Counts_1']
        self.us_jobs_model = DataStorage.job_model_dict['United States Jobs with Model US_0']
        self.ca_jobs_model = DataStorage.job_model_dict['Canada Jobs with Model Canada_0']
        self.job_iqr = DataStorage.job_iqr_dict['United States IQR US PayScale Main_0']
        self.rollup_iqr = DataStorage.job_iqr_dict['United States IQR US PSP Job Rollups_0']
        
        self.cfm_data = self.value_return()
        self.csv_write()

    @staticmethod
    def dictionary_try(dictionary, job):
        #If value not in dictionary return 0
        #Used for the two and four year dictionaries of job counts
        try:
            value = dictionary[job]
        except KeyError:
            value = 0
        return value

    @staticmethod
    def rollup_dictionary_try(dictionary, job):
        #Rollup Dictionary exception catcher
        #Used to return the job if the job is not in the dictionary
        try:
            value = dictionary[job]
        except KeyError:
            value = job
        return value

    @staticmethod
    def rollup_count_try(main_dictionary, roll, backup_dictionary):
        #Used for Rollup Counts
        #Returns 0 if not in dictionary
        try:
            value = main_dictionary[roll]
        except KeyError:
            #Reports changed. Used to use all jobs for the rollups but somewhere
            #the reports changed so I can no longer use 0 as a value.
            #value = 0

            try:
                value = backup_dictionary[roll]
            except KeyError:
                value = 0

        return value

    @staticmethod
    def iqr_count_try(dictionary, job):
        #used for the IQR Counts
        #Returns N/A of not in dictionary
        try:
            value = dictionary[job]
        except KeyError:
            value = 'N/A'

        return value

    @staticmethod
    def onet_code_try(dictionary, job):
        #used for the ONET Dictionary
        try:
            value = dictionary[job]
        except KeyError:
            value = 'N/A'

        if value == "":
            value = 'N/A'

        return value
        
    def reverse_rollup_lookup(self, job_in_question):

        task_count = 0

        try:
            answer_value = self.rollup_dict[job_in_question]
        except KeyError:
            answer_value = job_in_question

        try:
            all_jobs = self.task_jobs[answer_value]
        except KeyError:
            all_jobs = job_in_question

        for jobs in all_jobs:
            if jobs in self.tasks:
                task_count += 1

        return task_count

    def value_return(self):
        final_list = []
        category = None
        print "Creating the CFM Tab \n"
        for Job in self.current_jobs:
            two_year_us = self.dictionary_try(self.two_year_us_jobs, Job)
            four_year_us = self.dictionary_try(self.four_year_us_jobs, Job)
            two_year_ca = self.dictionary_try(self.two_year_canada_jobs, Job)
            four_year_ca = self.dictionary_try(self.four_year_canada_jobs, Job)
            if Job not in self.no_good_strings:
                category = 'Valid'
            elif Job in self.no_good_strings:
                category = 'Obsolete'
            rollup_title = self.rollup_dictionary_try(self.rollup_dict, Job)
            two_year_us_rollup = self.rollup_count_try(self.two_year_us_rollups, rollup_title, self.two_year_us_jobs)
            two_year_ca_rollup = self.rollup_count_try(self.two_year_ca_rollups, rollup_title,
                                                       self.two_year_canada_jobs)
            #four_year_us_rollup = self.rollup_count_try(self.four_year_us_rollups, rollup_title)
            #four_year_ca_rollup = self.rollup_count_try(self.four_year_ca_rollups, rollup_title)
            us_model = self.dictionary_try(self.us_jobs_model, rollup_title)
            ca_model = self.dictionary_try(self.ca_jobs_model, rollup_title)
            iqr_job = self.iqr_count_try(self.job_iqr, Job)
            iqr_rollup = self.iqr_count_try(self.rollup_iqr, rollup_title)
            rollup_have_tasks = None
            if Job in self.tasks:
                job_have_tasks = 'Yes'
            if Job not in self.tasks:
                job_have_tasks = 'No'
            if job_have_tasks == 'Yes':
                rollup_have_tasks = 'Yes'
            if job_have_tasks == 'No' and self.reverse_rollup_lookup(Job) == 0:
                rollup_have_tasks = 'No'
            if job_have_tasks == 'No' and self.reverse_rollup_lookup(Job) > 0:
                rollup_have_tasks = 'Yes'
            onet_breadth = self.onet_code_try(self.breadth_30, Job)
            
            final = Job, two_year_us, two_year_ca, four_year_us, four_year_ca, category, \
                rollup_title, two_year_us_rollup, two_year_ca_rollup, us_model, ca_model, \
                job_have_tasks, rollup_have_tasks, onet_breadth, iqr_job, iqr_rollup

            final_list.append(final)
        return final_list

    def csv_write(self):
        header = ['All Confirmed Job Titles', '2 Year Count (U.S.)', '2 Year Count (Canada)', '4 Year Count (U.S.)',
                  '4 Year Count (Canada)', 'Category', 'Rollup Title',
                  '2 Year Count for Rollup (U.S.)', '2 Year Count for Rollup (Canada)', 'U.S. Model Data Points',
                  'Canada Model Data Points', 'Job Have Tasks?', 'In Rollup with Job that has tasks?',
                  'SOC Code', 'IQR for Job (Target 20%)', 'IQR for Job Rollup  (Target 20%)']

        with open(WritingPath + 'CFM.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(header)
            for row in self.cfm_data:
                writer.writerow(row)

CreateCFMTab()

#Old Code to run through PSP Reports.
#Need to make this fancier and easier to read.


class PSPReportCompile:
    
    def __init__(self):
        self.current_months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        self.dates = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.results = []
        self.file_list = []
        self.one_year_of_reports()
        self.compile_reports()

    @staticmethod
    def insert(x):
        z = '.zip'
        return str(x).replace("(", "").replace(")", "").replace("'", "").replace(",", ".").replace(" ", "") + z

    def find_date_times_one_year_of_reports(self):

        today = datetime.datetime.now()

        a_year_ago = 'fancy'
    
    def one_year_of_reports(self):
        for i in range(12):  
            current_date = self.current_months[int(current_month)-i-1]
            if int(current_month) - i - 1 < 0:
                current_int_years = int(current_year) - 1
            else:
                current_int_years = int(current_year)
            value = str(current_int_years), str(current_date)
            value = self.insert(value)
            self.file_list.append(value)
    
    def compile_reports(self):
        print "Compiling the last year of PSP reports"
        for report_file in self.file_list:

            csv_report_name = report_file.replace(".zip", ".csv")

            test_file = zipfile.ZipFile(psp_file_path + report_file)
            test_file.extract(csv_report_name, working_directory)
            report_file = working_directory + '\\' + csv_report_name

            with open(report_file) as f:
                csv_file = csv.reader(f, delimiter=',')
                names = csv_file.next()
                
                print "Working on " + report_file

                for row in csv_file:
                    account_name = row[names.index('Name')]
                    account_id = row[names.index('Acct ID')]
                    subscription_type = row[names.index('SubscriptionType')]
                    job = row[names.index('Job')]

                    final = account_name, account_id, subscription_type, job

                    DataStorage.psp_reports.append(final)

            os.remove(report_file)

PSPReportCompile()

#Here layeth the beast of burden. The accounts tab code. At last run she had an error while calculating percentiles.
#Since no one ever looks at this measurement I'm commenting it out until we decide what we want do.
"""
class AccountsTab:
    
    def __init__(self):
        self.tenth = None
        self.median = None
        self.ninety = None
        self.ninety_fifth = None
        self.rollup_dict = rollup_mapping
        self.job_iqr = DataStorage.job_iqr_dict['United States IQR US PayScale Main_0']
        self.job_job_list = self.open_accounts_job_file()
        self.all_psp_rollups = []
        self.all_rollups_and_jobs = []
        self.map_jobs()
        self.rollup_counts = self.count_rollups()
        self.pull_all_rollups()
        self.all_rollups_and_jobs = list(set(self.all_rollups_and_jobs))
        self.iqr_distribution_dict = {}
        self.iqr_distribution()
        self.write_csv()

    @staticmethod
    def open_accounts_job_file():
        psp_accounts_list = []
        job_count_list = []

        for row in DataStorage.psp_reports:
            #psp_reports list is set up as Account Name, Acct ID, Subscription Type, Job (0,1,2,3)
            #If job is blank continue
            if row[3] == '':
                continue

            #job_job is job title, account name (0,1)
            job_job = row[3], row[0]
            psp_accounts_list.append(job_job)
        psp_accounts_list = list(set(psp_accounts_list))
        
        for job in psp_accounts_list:
            final = job[0]
            job_count_list.append(final)
            
        return job_count_list
                
    def map_jobs(self):
        for job in self.job_job_list:
            if job in self.rollup_dict:
                rollup = self.rollup_dict[job]
            elif job not in self.rollup_dict:
                rollup = job
            self.all_psp_rollups.append(rollup)
    
    def count_rollups(self):
        return coll.Counter(self.all_psp_rollups)

    def pull_all_rollups(self):
        with open(WritingPath + 'CFM.csv', 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            names = reader.next()
            for row in reader:
                rollup = row[names.index('Rollup Title')]
                self.all_rollups_and_jobs.append(rollup)
        
    def iqr_distribution(self):
        rollup_list = self.all_rollups_and_jobs
        iqr_list = []
        distribution = []

        for rollup in rollup_list:
            if rollup not in self.rollup_counts:
                continue

            elif rollup not in self.job_iqr:
                continue

            final = self.rollup_counts[rollup], self.job_iqr[rollup]
            iqr_list.append(final)
        
        for iqr in iqr_list:

            dist = [np.exp(float(iqr[1]))-1] * iqr[0]
            [distribution.append(X) for X in dist]
    
        self.tenth = np.percentile(distribution, 10)
        self.median = np.percentile(distribution, 50)
        self.ninety = np.percentile(distribution, 90)
        self.ninety_fifth = np.percentile(distribution, 95)
        
    def write_csv(self):
        print "Writing IQR Percentiles to file \n"
        with open(WritingPath + 'IQR.csv', 'wb') as f:
            writer = csv.writer(f, lineterminator='\n')
            header = ['Job \ Job', 'IQR']
            writer.writerow(header)
            for job in self.job_iqr:
                final = job, np.exp(float(self.job_iqr[job]))-1
                writer.writerow(final)
        
        with open(WritingPath + 'IQR Percentiles.csv', 'wb') as f:
            writer = csv.writer(f, lineterminator='\n')
            header = ['10th', '50th', '90th', '95th']
            writer.writerow(header)
            final = self.tenth, self.median, self.ninety, self.ninety_fifth
            writer.writerow(final)

AccountsTab()
"""

    
class UNCProfileExtractor:
    
    def __init__(self):
        for files in UNCFiles:
            print "Pulling data from " + files
            self.file = files
            self.job_count_dict = {}
            self.open_file(files)
            self.write_to_file(files)
    
    def open_file(self, files):

        with my_xml.report_handler(my_xml.RowNameEntryHandler) as handler:
            with open(ReportPath + files, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            self.job_count_dict = handler.count_dictionary
                    
    def write_to_file(self, files):
        if '_0' in files:
            DataStorage.unc_counts['United States 4 Year ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_count_dict
        if '_1' in files:
            DataStorage.unc_counts['Canada 4 Year ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_count_dict
        if '2_0' in files:
            DataStorage.unc_counts['United States 2 Year ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_count_dict
        if '2_1' in files:
            DataStorage.unc_counts['Canada 2 Year ' + files[len('Ryan Data Dashboard '):len(files)-4]] \
                = self.job_count_dict
            
UNCProfileExtractor()
            
            
class CreateUNCTab:
    
    def __init__(self):
        self.two_year_canada_jobs = DataStorage.unc_counts['Canada 4 Year List of Jobs not Deactivation Rules 2 year_1']
        self.four_year_canada_jobs = DataStorage.unc_counts['Canada 4 Year List of Jobs not Deactivation Rules 4 year_1']
        self.two_year_us_jobs = DataStorage.unc_counts['United States 4 Year List of Jobs not Deactivation Rules 2 year_0']
        self.four_year_us_jobs = DataStorage.unc_counts['United States 4 Year List of Jobs not Deactivation Rules 4 year_0']
        self.all_unc_jobs = self.gather_all_unc_jobs()
        self.cfm_data = self.value_return()
        self.csv_write()
            
    def gather_all_unc_jobs(self):
        unc_jobs_list = []
        us_jobs = self.four_year_us_jobs.keys()
        ca_jobs = self.four_year_canada_jobs.keys()
        [unc_jobs_list.append(Job) for Job in us_jobs]
        [unc_jobs_list.append(Job) for Job in ca_jobs]
        unc_jobs_list = list(set(unc_jobs_list))
        return unc_jobs_list

    @staticmethod
    def two_year(dictionary, job):
        #If value not in dictionary return <5
        #Used for the two year counts
        try:
            value = dictionary[job]
        except KeyError:
            value = '<5'
        return value

    @staticmethod
    def four_year(dictionary, job):
        #If value not in dictionary return <10
        #Used for the four year counts
        try:
            value = dictionary[job]
        except KeyError:
            value = '<10'
        return value

    def value_return(self):
        final_list = []
        for Job in self.all_unc_jobs:
            two_year_us = self.two_year(self.two_year_us_jobs, Job)
            four_year_us = self.four_year(self.four_year_us_jobs, Job)
            two_year_ca = self.two_year(self.two_year_canada_jobs, Job)
            four_year_ca = self.four_year(self.four_year_canada_jobs, Job)
            
            final = Job, two_year_us, four_year_us, two_year_ca, four_year_ca
            
            final_list.append(final)
            
        return final_list

    def csv_write(self):
        print "Writing the UNC Job tab to file \n"
        header = ['Unconfirmed Job Titles passing Deactivation Rules (Min U.S. 4 Year Count of 10)',
                  '2 Year Count (U.S.)', '4 Year Count (U.S.)', '2 Year Count (Canada)',
                  '4 Year Count (Canada)', 'Category']
        
        with open(WritingPath + 'UNC.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(header)
            for row in self.cfm_data:
                writer.writerow(row)

CreateUNCTab()


print "The Data Dashboard is complete. Your Welcome. \n"
print "-Ryan Patrick Henry Moore"
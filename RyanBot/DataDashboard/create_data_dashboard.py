import data_dashboard
import os
import csv
import datetime
import zipfile

out_directory = "\\\\filer01\\public\\Data Dashboards\\Temp Files\\Out Files\\"
writing_path = '\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\'
out_files = os.listdir(out_directory)


# #Pulling all admin tool data
# print "Setting up the data dashboard..."
dashboard = data_dashboard.DataDashboard()
# dashboard.pull_current_admin_tool_values()
# dashboard.write_breadth_thirty_to_file()
# dashboard.create_job_csv_files()
#
# #Running all analysis tool queries
# print "Running analysis tool queries..."
# dashboard.run_analysis_tool_overall_jobs_reports()
# dashboard.run_analysis_tool_rollups_queries()
# dashboard.run_model_queries()
# dashboard.run_iqr_queries()
# dashboard.run_analysis_tool_unconfirmed_queries()
#
# #Unzipping files
# print "Unzipping all of the analysis tool files..."
# dashboard.unzip_all_the_files()

#Extract XML Data
#Extracting Job Counts


for xml_files in out_files:

    if "Job Counts" in xml_files and ".xml" in xml_files:
        print "Pulling data from " + xml_files + "..."
        temp_dict = dashboard.extract_job_counts_from_xml(xml_files)

        if 'Four ' in xml_files and '_0' in xml_files:
            try:
                dashboard.job_count_dict['United States 4 Year Job Counts_0'].update(temp_dict)

            except KeyError:
                dashboard.job_count_dict['United States 4 Year Job Counts_0'] = {}

                dashboard.job_count_dict['United States 4 Year Job Counts_0'].update(temp_dict)

        if 'Four ' in xml_files and '_1' in xml_files:
            try:
                dashboard.job_count_dict['Canada 4 Year Job Counts_1'].update(temp_dict)

            except KeyError:
                dashboard.job_count_dict['Canada 4 Year Job Counts_1'] = {}

                dashboard.job_count_dict['Canada 4 Year Job Counts_1'].update(temp_dict)

        if 'Two ' in xml_files and '_0' in xml_files:
            try:
                dashboard.job_count_dict['United States 2 Year Job Counts Two_0'].update(temp_dict)

            except KeyError:
                dashboard.job_count_dict['United States 2 Year Job Counts Two_0'] = {}

                dashboard.job_count_dict['United States 2 Year Job Counts Two_0'].update(temp_dict)

        if 'Two ' in xml_files and '_1' in xml_files:
            try:
                dashboard.job_count_dict['Canada 2 Year Job Counts Two_1'].update(temp_dict)

            except KeyError:
                dashboard.job_count_dict['Canada 2 Year Job Counts Two_1'] = {}

                dashboard.job_count_dict['Canada 2 Year Job Counts Two_1'].update(temp_dict)

for xml_files in out_files:
    if "Job Rollup Counts" in xml_files and ".xml" in xml_files:
        print "Pulling data from " + xml_files + "..."
        temp_dict = dashboard.extract_job_counts_from_xml(xml_files)
        if 'Four' in xml_files and '_0' in xml_files:
            try:
                dashboard.job_count_dict['United States 4 Year Job Rollup Counts_0'].update(temp_dict)

            except KeyError:
                dashboard.job_count_dict['United States 4 Year Job Rollup Counts_0'] = {}

                dashboard.job_count_dict['United States 4 Year Job Rollup Counts_0'].update(temp_dict)

        if 'Four' in xml_files and '_1' in xml_files:
            try:
                dashboard.job_count_dict['Canada 4 Year Job Rollup Counts_1'].update(temp_dict)

            except KeyError:
                dashboard.job_count_dict['Canada 4 Year Job Rollup Counts_1'] = {}

                dashboard.job_count_dict['Canada 4 Year Job Rollup Counts_1'].update(temp_dict)

        if 'Two' in xml_files and '_0' in xml_files:
            try:
                dashboard.job_count_dict['United States 2 Year Job Rollup Counts Two_0'].update(temp_dict)

            except KeyError:
                dashboard.job_count_dict['United States 2 Year Job Rollup Counts Two_0'] = {}

                dashboard.job_count_dict['United States 2 Year Job Rollup Counts Two_0'].update(temp_dict)

        if 'Two' in xml_files and '_1' in xml_files:
            try:
                dashboard.job_count_dict['Canada 2 Year Job Rollup Counts Two_1'].update(temp_dict)

            except KeyError:
                dashboard.job_count_dict['Canada 2 Year Job Rollup Counts Two_1'] = {}

                dashboard.job_count_dict['Canada 2 Year Job Rollup Counts Two_1'].update(temp_dict)


for xml_files in out_files:
    if "IQR US PayScale Main" in xml_files and ".xml" in xml_files:
        print "Pulling data from " + xml_files + "..."
        temp_dict = dashboard.extract_current_iqr_data(xml_files)
        print temp_dict

        if '_0' in xml_files:
            try:
                dashboard.job_iqr_dict['United States IQR US PayScale Main_0'].update(temp_dict)

            except KeyError:
                dashboard.job_iqr_dict['United States IQR US PayScale Main_0'] = {}

                dashboard.job_iqr_dict['United States IQR US PayScale Main_0'].update(temp_dict)


for xml_files in out_files:
    if "IQR US PSP Job Rollups" in xml_files and ".xml" in xml_files:
        print "Pulling data from " + xml_files + "..."
        temp_dict = dashboard.extract_current_iqr_data(xml_files)

        dashboard.rollup_iqr_dict['United States IQR US PSP Job Rollups_0'] = temp_dict

for xml_files in out_files:
    if "Jobs with Model" in xml_files and ".xml" in xml_files:
        print "Pulling data from " + xml_files + "..."
        temp_dict = dashboard.extract_job_model_data(xml_files)
        if 'US' in xml_files:
            dashboard.job_model_dict['United States ' +
                                     xml_files[len('Ryan Data Dashboard '):len(xml_files)-4]] = temp_dict

        if 'Canada' in xml_files:
            dashboard.job_model_dict['Canada ' + xml_files[len('Ryan Data Dashboard '):len(xml_files)-4]] = temp_dict

for xml_files in out_files:
    if "List of Jobs not Deactivation" in xml_files and ".xml" in xml_files:
        print "Pulling data from " + xml_files + "..."
        temp_dict = dashboard.extract_unconfirmed_profile_data(xml_files)
        if 'List of Jobs not Deactivation Rules 2 year_0' in xml_files:
            dashboard.unc_counts['United States 4 Year List of Jobs not Deactivation Rules 2 year_0'] = temp_dict

        if 'List of Jobs not Deactivation Rules 2 year_1' in xml_files:
            dashboard.unc_counts['Canada 4 Year List of Jobs not Deactivation Rules 2 year_1'] = temp_dict

        if 'Ryan Data Dashboard List of Jobs not Deactivation Rules 4 year_0' in xml_files:
            dashboard.unc_counts['United States 4 Year List of Jobs not Deactivation Rules 4 year_0'] = temp_dict

        if 'List of Jobs not Deactivation Rules 4 year_1' in xml_files:
            dashboard.unc_counts['Canada 4 Year List of Jobs not Deactivation Rules 4 year_1'] = temp_dict


job_no_good = dashboard.return_no_good_strings_list()
rollup_mapping = dashboard.create_breadth_ten_rollup_dictionary()
task_rollup_mapping = dashboard.find_tasks_for_rollups()
current_jobs_list = dashboard.extract_jobs_from_file()
jobs_with_tasks = dashboard.extract_task_sets_from_file()
onet_breadth_thirty = dashboard.extract_breadth_thirty_data_from_file()

#The below code was ported from the archived version of the Data Dashboard. I don't have the time to re write this
#properly now and it seems to work fine so I'm leaving it. Tchus!


class CreateCFMTab:

    def __init__(self):
        self.current_jobs = current_jobs_list
        self.rollup_dict = rollup_mapping
        self.no_good_strings = job_no_good
        self.tasks = jobs_with_tasks
        self.breadth_30 = onet_breadth_thirty
        self.task_jobs = task_rollup_mapping
        self.two_year_canada_jobs = dashboard.job_count_dict['Canada 2 Year Job Counts Two_1']
        self.four_year_canada_jobs = dashboard.job_count_dict['Canada 4 Year Job Counts_1']
        self.two_year_us_jobs = dashboard.job_count_dict['United States 2 Year Job Counts Two_0']
        self.four_year_us_jobs = dashboard.job_count_dict['United States 4 Year Job Counts_0']
        self.two_year_us_rollups = dashboard.job_count_dict['United States 2 Year Job Rollup Counts Two_0']
        self.four_year_us_rollups = dashboard.job_count_dict['United States 4 Year Job Rollup Counts_0']
        self.two_year_ca_rollups = dashboard.job_count_dict['Canada 2 Year Job Rollup Counts Two_1']
        self.four_year_ca_rollups = dashboard.job_count_dict['Canada 4 Year Job Rollup Counts_1']
        self.us_jobs_model = dashboard.job_model_dict['United States Jobs with Model US_0']
        self.ca_jobs_model = dashboard.job_model_dict['Canada Jobs with Model Canada_0']
        self.job_iqr = dashboard.job_iqr_dict['United States IQR US PayScale Main_0']
        self.rollup_iqr = dashboard.rollup_iqr_dict['United States IQR US PSP Job Rollups_0']

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

        with open(writing_path + 'CFM.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(header)
            for row in self.cfm_data:
                writer.writerow(row)

CreateCFMTab()


#Old Code to run through PSP Reports.
#Need to make this fancier and easier to read.
now = str(datetime.datetime.now())
todays_date = now[:7]
current_year, current_month = todays_date.split("-")
todays_date = todays_date.replace('-', '')
todays_date_alt = now[:7]
psp_file_path = "\\\\filer01\\public\\Data Dashboards\\PSP Zip Reports\\"
working_directory = os.getcwd()

'''
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

                    dashboard.psp_reports.append(final)

            os.remove(report_file)
#PSPReportCompile()
'''

class CreateUNCTab:

    def __init__(self):
        self.two_year_canada_jobs = dashboard.unc_counts['Canada 4 Year List of Jobs not Deactivation Rules 2 year_1']
        self.four_year_canada_jobs = dashboard.unc_counts['Canada 4 Year List of Jobs not Deactivation Rules 4 year_1']
        self.two_year_us_jobs = \
            dashboard.unc_counts['United States 4 Year List of Jobs not Deactivation Rules 2 year_0']
        self.four_year_us_jobs = \
            dashboard.unc_counts['United States 4 Year List of Jobs not Deactivation Rules 4 year_0']
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

    @staticmethod
    def try_to_encode(str_):
        try:
            encoded = str_.encode("windows-1252")
        except:
            encoded = str_
        return encoded

    def csv_write(self):
        print "Writing the UNC Job tab to file \n"
        header = ['Unconfirmed Job Titles passing Deactivation Rules (Min U.S. 4 Year Count of 10)',
                  '2 Year Count (U.S.)', '4 Year Count (U.S.)', '2 Year Count (Canada)',
                  '4 Year Count (Canada)', 'Category']

        with open(writing_path + 'UNC.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(header)
            for row in self.cfm_data:
                try:
                    writer.writerow([CreateUNCTab.try_to_encode(x) for x in row])
                except:
                    continue

CreateUNCTab()


print "The Data Dashboard is complete. You're Welcome. \n"
print "-Ryan Patrick Henry Moore"

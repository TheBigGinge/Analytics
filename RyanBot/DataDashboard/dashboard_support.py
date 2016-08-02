import AnalysisTool.run_queries as rq
import DateFunctions.datetimes_in as dates
import RequestService.admin_requests as ad_req
import FileHandling.file_work as files
import AnalysisTool.extract_data_xml as extract
import csv


class DashboardSupport:

    def __init__(self):
        self.automated_files = "\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\"
        self.in_files = "\\\\filer01\\public\\Data Dashboards\\Temp Files\\In Files\\"
        self.out_files = "\\\\filer01\\public\\Data Dashboards\\Temp Files\\Out Files\\"

    def pull_all_current_job_rollups(self):

        rollup_list = []

        reader = files.FileHandler()

        for row in reader.open_tsv(self.automated_files + "Current Job Rollups.tsv"):

            rollup = row[reader.header.index("Read-only Answervalue")]
            if rollup != "":
                rollup_list.append(rollup)

        return list(set(rollup_list))

    def temp_pull_current_jobs(self):

        job_list = []

        reader = files.FileHandler()

        for row in reader.open_csv(self.automated_files + "Current Jobs.csv"):

            job_title = row[reader.header.index("ANSWER VALUE")]
            if job_title != "":
                job_list.append(job_title)

        return list(set(job_list))

    def pull_all_current_jobs(self):

        """This is not currently working. Something is wrong on the C# code side me thinks"""

        job_list = []

        reader = files.FileHandler()

        for row in reader.open_tsv(self.automated_files + "Current Jobs.tsv"):
            try:
                job_title = row[reader.header.index("ANSWER VALUE")]
                if job_title != "":
                    job_list.append(job_title)
            except IndexError:
                print row

        return list(set(job_list))

    def pull_current_admin_data(self):

        ad_req.PullAnyAffinityType(None,
                                   None,
                                   {'field': 'job', 'breadth': '10'},
                                   "Current Job Rollups",
                                   self.automated_files)

        ad_req.PullAnyAffinityType(None,
                                   "Unclassified",
                                   {'field': 'job'},
                                   "Current Unclassified",
                                   self.automated_files)

        ad_req.PullTaskSeedProfiles(self.automated_files + "Current Tasks.tsv")
        #TODO: Add in the Current Jobs.tsv when C# side is fixed

    def run_overall_table_queries(self, query_name, file_dim, table_dim, years, filter=""):
        """
        :param query_name:
            Title of the file you're going to create
        :param file_dim:
            The file dimension you want to build
        :param table_dim:
            The table dimension you want to build
        :param years:
            The number of years back you want the query to start
        """
        datage = dates.DateTimeFormats()

        end_date = str(datage.find_first_of_current_month().strftime("%Y-%m-%d"))
        start_date = str(datage.find_first_of_month_x_years_ago(years).strftime("%Y-%m-%d"))

        dash_reports = rq.AnonReports(self.in_files,
                                      self.out_files)

        dash_reports.post_analysis_tool_query_dim_list_create('psstats03',
                                                              query_name,
                                                              start_date,
                                                              end_date,
                                                              filter,
                                                              "Profile Age Measure",
                                                              'Count',
                                                              file_dim,
                                                              table_dim,
                                                              )

    def run_iqr_queries(self, query_name, file_dim, table_dim, years):
        """
        :param query_name:
            Title of the file you're going to create
        :param file_dim:
            The file dimension you want to build
        :param table_dim:
            The table dimension you want to build
        :param years:
            The number of years back you want the query to start
        """

        main_filter = 'Location\Country\United States{match,1,0} & survey\survey\PayScale Main{match,1,0}'
        datage = dates.DateTimeFormats()

        end_date = str(datage.find_first_of_current_month().strftime("%Y-%m-%d"))
        start_date = str(datage.find_first_of_month_x_years_ago(years).strftime("%Y-%m-%d"))

        dash_reports = rq.AnonReports(self.in_files,
                                      self.out_files)

        dash_reports.post_analysis_tool_query_dim_list_create('localhost',
                                                              query_name,
                                                              start_date,
                                                              end_date,
                                                              main_filter,
                                                              "Combined TCC IQR Measure",
                                                              'Median',
                                                              file_dim,
                                                              table_dim,
                                                              )

    def run_model_data_queries(self):

        dash_reports = rq.AnonReports(self.in_files, self.out_files)

        dash_reports.post_analysis_tool_model_report("localhost",
                                                     "Ryan Data Dashboard Jobs with Model Canada",
                                                     "CA")

        dash_reports.post_analysis_tool_model_report("localhost",
                                                     "Ryan Data Dashboard Jobs with Model US",
                                                     "US")

    def run_unconfirmed_data_queries(self, query_name, file_dim, table_dim, years):

        filter = 'profile\\profilewizardid{irange,3,0,5,5} & !(affinityid\\12883618{match,1,0} | ' \
                 'affinityid\\12883619{match,1,0} | affinityid\\12883620{match,1,0} |' \
                 ' affinityid\\12883621{match,1,0} | affinityid\\12883625{match,1,0} | ' \
                 'affinityid\\12883626{match,1,0} | affinityid\\12883627{match,1,0} | ' \
                 'affinityid\\12883628{match,1,0} | affinityid\\12883629{match,1,0} | ' \
                 'affinityid\\12883630{match,1,0} | affinityid\\12883631{match,1,0} | ' \
                 'affinityid\\12883632{match,1,0} | affinityid\\12883633{match,1,0} | ' \
                 'affinityid\\12883634{match,1,0} | affinityid\\12883636{match,1,0} | ' \
                 'affinityid\\12883638{match,1,0} | affinityid\\12883639{match,1,0} | ' \
                 'affinityid\\12883640{match,1,0}){999,d,0,0}'

        datage = dates.DateTimeFormats()

        end_date = str(datage.find_first_of_current_month().strftime("%Y-%m-%d"))
        start_date = str(datage.find_first_of_month_x_years_ago(years).strftime("%Y-%m-%d"))

        dash_reports = rq.AnonReports(self.in_files, self.out_files)

        dash_reports.post_analysis_tool_count_table_report("psbuilder02a",
                                                           query_name,
                                                           start_date,
                                                           end_date,
                                                           filter,
                                                           first_dimension_list=file_dim,
                                                           second_dimension_list=table_dim)

    def break_up_jobs_file(self):
        #Anon analysis tool reports seem to fail if there's more than 4 or 5k jobs
        #splitting up jobs between queries
        jobs_list = []
        job_file = files.FileHandler()
        file_count = 1
        row_count = 0

        for row in job_file.open_csv(self.automated_files + "Current Jobs.csv"):
            row_count += 1

        for i, row in enumerate(job_file.open_csv(self.automated_files + "Current Jobs.csv")):
            main_job = row[job_file.header.index("ANSWER VALUE")]
            jobs_list.append(main_job)
            if (i % 3000 == 0 and i != 0) or i == row_count - 1:
                with open(self.automated_files + "Current Jobs_" + str(file_count) + ".csv", 'wb') as W:
                    writer = csv.writer(W, delimiter=',')
                    header = "ANSWER VALUE", ""
                    writer.writerow(header)

                    for job in jobs_list:
                        final_job = job, ""
                        writer.writerow(final_job)

                file_count += 1
                jobs_list = []

    def pull_task_rollup_combos(self):

        rollup_dict = {}

        with open(self.automated_files + 'Current Job Rollups.tsv', 'rb') as f:
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

    def create_full_task_dictionary(self):
        print "Gathering all tasks into a job to task dictionary..."
        handler = files.FileHandler()
        task_dict = {}
        for line in handler.open_csv(self.automated_files + 'Current Tasks.csv'):
            job = line[handler.header.index("JOB")]
            tasks = line[handler.header.index("TASK")]

            try:
                task_dict[job] += " " + tasks.lower()
            except KeyError:
                task_dict[job] = tasks.lower()

        return task_dict

    def create_deduped_task_dictionary(self):
        task_dict = {}

        with open(self.automated_files + 'Current Tasks.csv', 'rb') as R:
            reader = csv.reader(R, delimiter='\t')
            names = reader.next()

            for row in reader:
                title = row[names.index("JobRollup")].lower()
                task = row[names.index("Task")]

                if title not in task_dict.keys():
                    task_dict[title] = []
                    task_dict[title].append(task)
                else:
                    task_dict[title].append(task)

        for key in task_dict:
            task_list = task_dict[key]
            deduped = list(set(task_list))
            task_dict[key] = deduped

        return task_dict


    @staticmethod
    def pull_no_good_strings():

        print "Pulling the NG Strings list \n"
        ng_path = 'C:\\hg\\payscale\\data\\AnswerSearch\\'
        ng_file = 'Job.nogood'
        ng_strings_list = []
        with open(ng_path + ng_file, 'rb') as f:
            for line in f:
                ng_string = line.strip('\r\n')
                ng_strings_list.append(ng_string)
        return ng_strings_list

    def pull_jobs_and_rollups_to_dict(self):

        print "Finding the Current Rollups List \n"
        rollup_dict = {}
        with open(self.automated_files + 'Current Job Rollups.tsv', 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            names = reader.next()
            for row in reader:
                rule_value = row[names.index('RULE VALUE')]
                answer_value = row[names.index('Read-only Answervalue')]
                rollup_dict[rule_value] = answer_value
        return rollup_dict

    def full_job_to_job_rollup_map(self):

        job_rollup_mapping = {}
        breadth_10_map = self.pull_jobs_and_rollups_to_dict()

        all_jobs = self.temp_pull_current_jobs()

        for job_title in all_jobs:
            try:
                rollup = breadth_10_map[job_title]
            except KeyError:
                rollup = job_title

            job_rollup_mapping[job_title] = rollup

        return job_rollup_mapping

    def create_breadth_thirty_file(self):

        breadth_thirty = []

        print "Building the Current Breadth 30 tab..."
        with open(self.automated_files + "Current Unclassified.tsv", 'rb') as R:
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

        with open(self.automated_files + "Current Job Rollups.tsv", 'rb') as R:
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

        with open(self.automated_files + "Current Breadth 30.csv", 'w') as W:
            writer = csv.writer(W, lineterminator='\n')

            header = ['Affinity Name', 'Job/Job AV', 'PSP AV (Breadth 10 Affinities)', 'SOC Code',
                      'Classified in Breadth 30?']

            writer.writerow(header)

            for line in breadth_thirty:
                writer.writerow(line)

    def unzip_file(self, zip_file, out_file = None):

        if out_file == None:
            files.FileHandler().zip_file_open(zip_file, self.out_files)
        else:
            files.FileHandler().zip_file_open(zip_file, out_file)

    def pull_tasks_from_file(self):

        print "Pulling Jobs with Current Tasks \n"
        task_set = set()
        with open(self.automated_files + 'Current Tasks.csv', 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            names = reader.next()
            for row in reader:
                job = row[names.index('JOB')]
                task_set.add(job)

        return task_set

    def pull_breadth_thirty_from_file(self):

        print "Pulling Breadth 30 Rollups \n"
        onet_dict = {}
        with open(self.automated_files + 'Current Breadth 30.csv', 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            names = reader.next()
            for row in reader:
                job_job = row[names.index('Job/Job AV')]
                classification = row[names.index('SOC Code')]

                if classification == "" and job_job in onet_dict.keys():
                    continue

                onet_dict[job_job] = classification

        return onet_dict

    @staticmethod
    def pull_job_data_from_xml(xml_file):

        return extract.ExtractXMLData(xml_file).overall_data_count()

    @staticmethod
    def pull_iqr_data_from_xml(xml_file):

        return extract.ExtractXMLData(xml_file).iqr_content_handler()

    @staticmethod
    def pull_unconfirmed_data_from_xml(xml_file):

        return extract.ExtractXMLData(xml_file).row_name_entry_handler()

    @staticmethod
    def pull_model_data_from_xml(xml_file):

        return extract.ExtractXMLData(xml_file).model_content_handler()
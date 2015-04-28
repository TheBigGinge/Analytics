import os
import sys
sys.path.append("C:\\hg\\payscale\\users\\ryanm\\PayScaleAnalytics\\")
import AnalysisTool.deserialize_xml as my_xml
import dashboard_support as ds


class DataDashboard:

    job_count_dict = {}
    job_iqr_dict = {}
    rollup_iqr_dict = {}
    job_model_dict = {}
    psp_reports = []
    unc_counts = {}

    def __init__(self):
        """
        This is the class that calls the admin and analysis tool
        to pull all the data used for the Taxonomy Data Dashboard
        """
        self.automated_file_path = '\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\'
        self.out_file = '\\\\filer01\\public\\Data Dashboards\\Temp Files\\Out Files\\'

    def run_analysis_tool_overall_jobs_reports(self):

        query = ds.DashboardSupport()
        job_files = []
        dash_files = os.listdir(self.automated_file_path)

        [job_files.append(files) for files in dash_files if "Current Jobs_" in files]

        for i, job_file in enumerate(job_files):

            query.run_overall_table_queries("Ryan Data Dashboard Job Counts Two " + str(i),
                                            "US and Canada",
                                            "Current Jobs_" + str(i + 1) + ".csv",
                                            2)

            query.run_overall_table_queries("Ryan Data Dashboard Job Counts Four " + str(i),
                                            "US and Canada",
                                            "Current Jobs_" + str(i + 1) + ".csv",
                                            4)

    @staticmethod
    def run_analysis_tool_unconfirmed_queries():

        query = ds.DashboardSupport()

        query.run_unconfirmed_data_queries("Ryan Data Dashboard List of Jobs not Deactivation Rules 2 year",
                                           "US and Canada",
                                           "Survey PayScale Main",
                                           2)

        query.run_unconfirmed_data_queries("Ryan Data Dashboard List of Jobs not Deactivation Rules 4 year",
                                           "US and Canada",
                                           "Survey PayScale Main",
                                           4)


    @staticmethod
    def run_analysis_tool_rollups_queries():

        query = ds.DashboardSupport()

        query.run_overall_table_queries("Ryan Data Dashboard Job Rollup Counts Two",
                                        "US and Canada",
                                        "Current Rollups.csv",
                                        2)

        query.run_overall_table_queries("Ryan Data Dashboard Job Rollup Counts Four",
                                        "US and Canada",
                                        "Current Rollups.csv",
                                        4)

    def run_iqr_queries(self):

        query = ds.DashboardSupport()
        job_files = []
        dash_files = os.listdir(self.automated_file_path)

        [job_files.append(files) for files in dash_files if "Current Jobs_" in files]
        '''
        query.run_iqr_queries("Ryan Data Dashboard IQR US PSP Job Rollups",
                              None,
                              "Current Rollups.csv",
                              2)
        '''
        for i, job_file in enumerate(job_files):
            query.run_iqr_queries("Ryan Data Dashboard IQR US PayScale Main " + str(i),
                                  None,
                                  "Current Jobs_" + str(i + 1) + ".csv",
                                  2)

    @staticmethod
    def run_model_queries():

        query = ds.DashboardSupport()

        query.run_model_data_queries()

    def extract_job_counts_from_xml(self, files):

        my_xml.fix_xml_encoding(self.out_file, files)

        return ds.DashboardSupport().pull_job_data_from_xml(self.out_file + files)

    def extract_current_iqr_data(self, files):

        my_xml.fix_xml_encoding(self.out_file, files)

        return ds.DashboardSupport().pull_iqr_data_from_xml(self.out_file + files)

    @staticmethod
    def pull_current_admin_tool_values():

        ds.DashboardSupport().pull_current_admin_data()

    @staticmethod
    def find_tasks_for_rollups():

        return ds.DashboardSupport().pull_task_rollup_combos()

    @staticmethod
    def return_no_good_strings_list():

        return ds.DashboardSupport().pull_no_good_strings()

    @staticmethod
    def create_breadth_ten_rollup_dictionary():

        return ds.DashboardSupport().pull_jobs_and_rollups_to_dict()

    @staticmethod
    def create_all_rollup_dictionary():

        return ds.DashboardSupport().full_job_to_job_rollup_map()

    @staticmethod
    def extract_jobs_from_file():
        #TODO: Find out why the tsv version is messed up
        return ds.DashboardSupport().temp_pull_current_jobs()

    @staticmethod
    def extract_task_sets_from_file():

        return ds.DashboardSupport().pull_tasks_from_file()

    @staticmethod
    def extract_breadth_thirty_data_from_file():

        return ds.DashboardSupport().pull_breadth_thirty_from_file()

    def extract_job_model_data(self, files):

        my_xml.fix_xml_encoding(self.out_file, files)

        return ds.DashboardSupport().pull_model_data_from_xml(self.out_file + files)

    def extract_unconfirmed_profile_data(self, files):

        my_xml.fix_xml_encoding(self.out_file, files)

        return ds.DashboardSupport().pull_unconfirmed_data_from_xml(self.out_file + files)

    @staticmethod
    def write_breadth_thirty_to_file():

        ds.DashboardSupport().create_breadth_thirty_file()

    def unzip_all_the_files(self):

        for zip_files in os.listdir(self.out_file):
            if ".zip" in zip_files:
                ds.DashboardSupport().unzip_file(zip_files)

    @staticmethod
    def create_job_csv_files():

        ds.DashboardSupport().break_up_jobs_file()
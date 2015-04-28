import AnalysisTool.run_queries as rq
import AnalysisTool.extract_data_xml as extract
import RyanBot.DataDashboard.data_dashboard as dd
import DateFunctions.datetimes_in as di
import FileHandling.file_work as fw


class SuggestionHelper:

    def __init__(self):
        self.temp_in_files = '\\\\filer01\\public\\Data_Analytics\\Job Rollup Suggesting\\TempFiles\\TempIn\\'
        self.temp_out_files = '\\\\filer01\\public\\Data_Analytics\\Job Rollup Suggesting\\TempFiles\\TempOut\\'

    def run_analysis_tool(self):
        dates = di.DateTimeFormats()
        end_date = dates.find_first_of_current_month().strftime("%Y-%m-%d")
        start_date = dates.find_first_of_month_x_years_ago(2).strftime("%Y-%m-%d")

        query = rq.AnonReports(self.temp_in_files, self.temp_out_files)
        query.post_analysis_tool_query_dim_list_create('localhost',
                                                       'Ryan Job Rollup Suggestor EAC',
                                                       start_date,
                                                       end_date,
                                                       'Location\\Country\\United States{match,1,0}',
                                                       'EAC Measure',
                                                       'Medians',
                                                       first_dimension_list=None,
                                                       second_dimension_list=self.pull_jobs_no_rollups(),
                                                       string_builder_type='Job')

    def extract_data(self):

        print "Unzipping and modifying Analysis Tool results..."
        fw.FileHandler().zip_file_open('Ryan Job Rollup Suggestor EAC.zip', self.temp_out_files)
        extract.ExtractXMLData('Ryan Job Rollup Suggestor EAC_0.xml').fix_xml_encoding(self.temp_out_files)
        count_dict = extract.ExtractXMLData(self.temp_out_files + 'Ryan Job Rollup Suggestor EAC_0.xml')\
            .overall_medians_list_return()

        return count_dict


    @staticmethod
    def pull_jobs_no_rollups():
        return_list = []

        dash = dd.DataDashboard()
        all_jobs = dash.extract_jobs_from_file()
        all_breadth_10 = dash.create_breadth_ten_rollup_dictionary()

        all_classified = all_breadth_10.keys()

        for job in all_jobs:
            if "Marine Corp" in job or "Navy" in job or "Army" in job or "Coast Guard" in job:
                continue
            elif job in all_classified:
                continue
            else:
                return_list.append(job)

        return return_list


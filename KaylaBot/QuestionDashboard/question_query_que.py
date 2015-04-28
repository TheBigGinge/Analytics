import AnalysisTool.run_queries as build
import datetime
import calendar


input_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\input_files\\"
output_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\output_files\\"
file_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\"


class BuildQueries:

    def __init__(self, min_date):
        self.min_date = min_date
        self.start_date = None
        self.end_date = None
        self.fix_dates()

    def fix_dates(self):

        month = self.min_date.month()
        year = self.min_date.year()
        last_day = calendar.monthrange(year, month)
        self.start_date = str(datetime.datetime(year, month, 1).strftime("%Y-%m-%d"))
        self.end_date = str(datetime.datetime(year, month, last_day[1]).strftime("%Y-%m-%d"))

    def main_query_build(self):
        main_filter = "(Profile\ProfileType\JobOffer{match,1,0} | Profile\ProfileType\CurrentJob{match,1,0}){999,d,0,0}"

        build.AnonReports(input_path, output_path)\
            .post_analysis_tool_query_dim_list_create("localhost",
                                                      "Kayla Question Activation Counts",
                                                      self.start_date,
                                                      self.end_date,
                                                      main_filter,
                                                      "Profile Age Measure",
                                                      "Count",
                                                      file_path + "All_Questions.csv",
                                                      None,
                                                      dimension="ONET 30 Dimension",
                                                      string_builder_type="Question")
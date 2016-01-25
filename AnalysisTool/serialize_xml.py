import xml.etree.cElementTree as ET
import csv
import os
import DateFunctions.datetimes_in as df
import xml.dom.minidom as minidom

automated_dashboard_path = '\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\'


class BuildOverallTableXML:

    """
    Designed to build an XML file that you can send to the Analysis Tool RESTFul webservice.
    No more hand cranking involved if you can create an instance of your Analysis Tool file and
    then update it when needed.

    !!!SAVE THE output_file WITH THE .ac.txt ENDING!!!

    Here's an example How To:
        BuildOverallTableXML("localhost", "Ryan Data Dashboard Job Rollup Counts 2", '2014-02-01',
                             '2014-03-01', "C:\\users\\ryanm\\desktop\\Ryan Analysis Tool Test.ac.txt",
                             first_dimension_list=None,
                             second_dimension_list="Current Jobs Test.csv").build_overall_table_counts_file()
    """
    def __init__(self, index_server,
                 input_file,
                 min_date,
                 max_date,
                 output_file,
                 main_filter="",
                 report_definition="OverallTableDefinition",
                 report_measure="EAC Measure",
                 fitting="Data",
                 return_type="Count",
                 first_dimension_list=None,
                 second_dimension_list=None,
                 first_dimension_file=None,
                 second_dimension_file=None,
                 part_time='true',
                 pfgid='false',
                 dimension=None,
                 ranges="Fixed",
                 confirmed="ConfirmedOnly",
                 row_count="0",
                 min_per_row="0",
                 string_builder_type=None):
        """
        :param index_server:
            index server you'd like the machine to point at (localhost, psstats03, etc)
        :param input_file:
            The name of the analysis tool query
        :param min_date:
            Min date as in the Analysis Tool such as 1/1/2000
        :param max_date:
            Max date as in the Analysis Tool such as 1/1/2100
        :param output_file:
            Directory where  you want the xml document to be pooped out
        :param main_filter:
            The large text filter on the main AnalysisTool.aspx page
        :param report_definition:
            The different types of report definitions (OverallTableDefinition, CountTableDefinition, etc)
        :param report_measure:
            The dimensions (EAC Dimension, Profile Age Dimension, Skill Dimension, etc)
        :param fitting:
            If using a measure (data, fitted, trimmed, etc)
        :param return_type:
            The columns drop down (Medians, Count, Median, etc)
        :param first_dimension_list:
            File Dimension
        :param second_dimension_list:
            Table Dimension
        :param first_dimension_file:
            Dimension files are pre-saved dimension files that are built in psstats03.
            If you do not put in an already created dimension file then bad stuff will happen!
        :param second_dimension_file:
            Dimension files are pre-saved dimension files that are built in psstats03.
            If you do not put in an already created dimension file then bad stuff will happen!
        :param part_time:
            true if you want the part time button checked
        :param pfgid:
            true if you want the pfgid button checked
        :param dimension:
            This is the count table definition you would use for a Table Dimension query.
            Example: report_definition = TableDimension, report_measure = Profile Age Measure, dimension = Job Rollup
        :return:
            Text file of the analysis config xml
        """
        self.min_date = min_date + "T00:00:00"
        self.max_date = max_date + "T00:00:00"
        self.output_file = output_file
        self.index_server = index_server
        self.input_file = input_file
        self.main_filter = main_filter
        self.report_definition = report_definition
        self.report_measure = report_measure
        self.fitting = fitting
        self.return_type = return_type
        self.first_dimension_file = first_dimension_file
        self.second_dimension_file = second_dimension_file
        self.first_dimension_list = first_dimension_list
        self.second_dimension_list = second_dimension_list
        self.part_time = part_time
        self.pfgid = pfgid
        self.dimension = dimension
        self.ranges = ranges
        self.confirmed = confirmed
        self.row_count = row_count
        self.min_per_row = min_per_row
        self.string_builder_type = string_builder_type

    def build_overall_table_counts_file(self):

        root = ET.Element("AnalysisConfig")
        root.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
        root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

        index_server = ET.SubElement(root, 'IndexServer')
        index_server.text = self.index_server

        name = ET.SubElement(root, 'Name')
        name.text = self.input_file

        text_filter = ET.SubElement(root, 'Filter')
        text_filter.text = self.main_filter

        report_def = ET.SubElement(root, 'ReportDef')
        report_def.set('xsi:type', self.report_definition)
        #The Name parameter is apparently not required
        #report_def.set("Name", "Average EAC Overall")

        measure = ET.SubElement(report_def, 'Measure')
        under_measure = ET.SubElement(measure, 'Measure')
        under_measure.set('Ref', self.report_measure)

        fitting = ET.SubElement(measure, "Fitting")
        fitting.text = self.fitting

        columns = ET.SubElement(report_def, 'Columns')
        columns.text = self.return_type

        if self.dimension is None:
            self.build_report_definition(report_def)

        else:
            self.build_table_dimension(report_def)
            summarize = ET.SubElement(report_def, 'Summarize')
            summarize.text = "false"

        if self.first_dimension_file is None:
            dim_1_list = ET.SubElement(root, 'Dim1List')
            self.dimension_list_build(dim_1_list, 1)
        else:
            dim_1_file = ET.SubElement(root, 'Dim1File')
            dim_1_file.text = self.first_dimension_file

        if self.second_dimension_file is None:
            dim_2_list = ET.SubElement(root, 'Dim2List')
            self.dimension_list_build(dim_2_list, 2)
        else:
            dim_2_file = ET.SubElement(root, 'Dim2File')
            dim_2_file.text = self.second_dimension_file

        part_time = ET.SubElement(root, 'PartTime')
        part_time.text = self.part_time

        unique = ET.SubElement(root, 'Unique')
        unique.text = 'false'   # ATH 1/22/2016 changed to false

        no_profile_list = ET.SubElement(root, 'NoProfileLists')
        no_profile_list.text = 'true'

        pfgid = ET.SubElement(root, 'PFGID')
        pfgid.text = self.pfgid

        show_report_error = ET.SubElement(root, 'ShowReportErrors')
        show_report_error.text = 'false'

        currency = ET.SubElement(root, 'Currency')
        currency.text = 'U.S. Dollar (USD)'

        min_date = ET.SubElement(root, 'MinDate')
        min_date.text = self.min_date

        max_date = ET.SubElement(root, 'MaxDate')
        max_date.text = self.max_date

        last_run = ET.SubElement(root, 'LastRunDate')
        last_run.text = str(df.DateTimeFormats().return_today_as_y_m_d("-")) + "T00:00:00"

        exp_date = ET.SubElement(root, 'ExpirationDate')
        exp_date.text = str(df.DateTimeFormats().return_today_as_y_m_d("-")) + "T00:00:00"

        max_results = ET.SubElement(root, 'MaxResults')
        max_results.text = '1000000'

        alt_search = ET.SubElement(root, 'AltSearchMode')
        alt_search.text = ""

        tree = ET.ElementTree(root)
        tree.write(self.output_file, "utf-8", "1.0")

    @staticmethod
    def build_report_definition(report_def):

            show_empty = ET.SubElement(report_def, 'ShowEmptyRows')
            show_empty.text = 'true'

            min_count = ET.SubElement(report_def, 'MinCountPerRow')
            min_count.text = '0'

            compare_row = ET.SubElement(report_def, 'ComparisonRow')
            compare_row.text = 'Auto'

            show_data = ET.SubElement(report_def, 'ShowData')
            show_data.text = 'false'

            show_raw = ET.SubElement(report_def, 'ShowRawData')
            show_raw.text = 'false'

    def build_table_dimension(self, report_def):

            dimension = ET.SubElement(report_def, 'Dimension')

            dimension_name = ET.SubElement(dimension, 'Dimension')
            dimension_name.set('Ref', self.dimension)

            ranges = ET.SubElement(dimension, 'Ranges')
            ranges.text = self.ranges

            confirmed = ET.SubElement(dimension, 'Filter')
            confirmed.text = self.confirmed

            row_count = ET.SubElement(dimension, 'RowCount')
            row_count.text = self.row_count

            min_per_row = ET.SubElement(dimension, 'MinPerRow')
            min_per_row.text = self.min_per_row

    def dimension_list_build(self, dimension_list, number_of_list):

        if number_of_list == 1:
            file_to_use = self.first_dimension_list
        else:
            file_to_use = self.second_dimension_list

        if file_to_use is None or file_to_use is "":
            string = ET.SubElement(dimension_list, 'string')
            string.text = "AS[.]ALL"
            #as future reference the AS[.]ALL dimension file equivalent
            #is "&amp;&amp; ALL" in case you want to go that direction

        else:
            self.build_quick_dimension_lists(file_to_use, dimension_list)

    def build_quick_dimension_lists(self, file_to_use, dimension_list):

        #assert os.path.isfile(file_to_use) is True, "For Dimension lists you need to give the Build OverTableXml " \
        #                                            "class a file. This is not a file: " + file_to_use

        if "Current Jobs" in file_to_use:
            self.create_job_answer_values(file_to_use, dimension_list)

        elif "Current Rollups" in file_to_use:
            self.create_rollup_answer_values(file_to_use, dimension_list)

        elif "Current Jobs Test.csv" in file_to_use:
            #obviously just used for testing
            #This test file only has two jobs in it so I could get results
            #back very fast
            self.create_job_answer_values(file_to_use, dimension_list)

        elif isinstance(file_to_use, list) and file_to_use[0] == 'Certifications/Certifications':
            self.mobile_survey_list_create(dimension_list, file_to_use)

        elif isinstance(file_to_use, list) and self.string_builder_type == 'Job':
            self.create_job_jobs_from_list(dimension_list, file_to_use)

        elif "Survey PayScale Main" in file_to_use:
            self.create_survey_dimension(dimension_list)

        elif "Country Dimension.csv" in file_to_use:
            try:
                with open(automated_dashboard_path + file_to_use, 'rb') as R:
                    reader = csv.reader(R, delimiter=',')

                    names = reader.next()

                    for row in reader:
                        answer_string = row[names.index('Answer Value')].strip()
                        string = ET.SubElement(dimension_list, 'string')
                        string.text = answer_string

            except IOError:
                print "Couldn't open your file " + file_to_use

        elif self.string_builder_type == "Question":
            self.create_question_answer_values(file_to_use, dimension_list)

        elif "US and Canada" in file_to_use:
            string = ET.SubElement(dimension_list, 'string')
            string.text = "AS[.]AV{Location\Country\United States}"
            string = ET.SubElement(dimension_list, 'string')
            string.text = "AS[.]AV{Location\Country\Canada}"


        # ATH 11/2/2015

        elif isinstance(file_to_use, list) and file_to_use[0] == r'Profile ID List':
            answer_string = "AS[profiles]"
            for i, profile_id in enumerate(file_to_use[1:], start=1):
                answer_string += "AV{Profile\\ID\\" + str(profile_id) + "}"
                if i < len(file_to_use[1:]):
                    answer_string += " + "
            string = ET.SubElement(dimension_list, 'string')
            string.text = answer_string
            # print answer_string
            # print string.text

        elif isinstance(file_to_use, list) and file_to_use[0] == r'Dimensions Formatted':
            list_of_dimensions = file_to_use[1:]
            for dimension in list_of_dimensions:
                string = ET.SubElement(dimension_list, 'string')
                string.text = dimension
                # print dimension


    @staticmethod
    def create_job_jobs_from_list(dimension_list, file_to_use):
        for job in file_to_use:
            string = ET.SubElement(dimension_list, 'string')
            string.text = "AS[" + job + "]AV{job\\job\\" + job + "}"

    @staticmethod
    def mobile_survey_list_create(dimension_list, file_to_use):

        for question in file_to_use:
            split = question.partition("/")
            fore = split[0]
            aft = split[2]
            answer_string = "AS[" + aft + "]ANY{" + fore + "\\" + aft + "}"
            string = ET.SubElement(dimension_list, 'string')
            string.text = answer_string

    @staticmethod
    def create_survey_dimension(dimension_list):

        string = ET.SubElement(dimension_list, 'string')
        string.text = "AS[PayScale Main]AV{Survey\Survey\PayScale Main}"

    @staticmethod
    def create_rollup_answer_values(file_to_use, dimension_list):

        try:
            rollups = []
            with open(automated_dashboard_path + file_to_use, 'rb') as R:
                reader = csv.reader(R, delimiter=',')

                names = reader.next()

                for row in reader:
                    rollup_title = row[names.index('Read-only Answervalue')].strip()
                    if rollup_title != "":
                        rollups.append(rollup_title)

                rollups = list(set(rollups))

                for rollup in rollups:
                    answer_string = "AS[" + rollup + "]AV{Job\\Job.Rollup\\" + rollup + "}"
                    string = ET.SubElement(dimension_list, 'string')
                    string.text = answer_string

        except IOError:
            print "Couldn't open your file " + file_to_use

    @staticmethod
    def create_job_answer_values(file_to_use, dimension_list):

        try:
            with open(automated_dashboard_path + file_to_use, 'rb') as R:
                reader = csv.reader(R, delimiter=',')

                names = reader.next()

                for row in reader:
                    answer_string = row[names.index('ANSWER VALUE')].strip()
                    answer_string = "AS[" + answer_string + "]AV{Job\\Job\\" + answer_string + "}"
                    string = ET.SubElement(dimension_list, 'string')
                    string.text = answer_string

        except IOError:
            print "Couldn't open your file " + file_to_use

    @staticmethod
    def create_question_answer_values(file_to_use, dimension_list):

        try:
            with open(file_to_use, 'rb') as R:
                reader = csv.reader(R, delimiter=',')

                for row in reader:
                    if "All Questions" not in row[0]:
                        answer_string = "AS[" + row[0] + "]ANY{" + row[0].replace("/", "\\") + "}"
                        string = ET.SubElement(dimension_list, 'string')
                        string.text = answer_string
        except IOError:
            print "Couldn't open your file " + file_to_use


class BuildMVariateViewDefinition:

    """
    Specifically designed for model reports.
    Mostly because that's the only thing we use this for.
    It would be very easy to set this up to do custom reports if we ever find
    anything else we need this for.
    """

    def __init__(self,
                 index_server,
                 input_file,
                 output_file,
                 country):

        self.min_date = "2000-01-01T00:00:00"
        self.max_date = "2100-01-01T00:00:00"
        self.output_file = output_file
        self.index_server = index_server
        self.input_file = input_file
        self.country = country

        assert self.country in ["CA", "US"], "Country needs to be a string of either US or CA"

    def build_xml_file(self):

        root = ET.Element("AnalysisConfig")
        root.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
        root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

        index_server = ET.SubElement(root, 'IndexServer')
        index_server.text = self.index_server

        name = ET.SubElement(root, 'Name')
        name.text = self.input_file

        text_filter = ET.SubElement(root, 'Filter')
        text_filter.text = "job\\job\\forester{match,1,0}"

        report_def = ET.SubElement(root, 'ReportDef')
        report_def.set('xsi:type', "MVariateViewDefinition")

        source = ET.SubElement(report_def, "Source")
        source.set("xsi:type", "ModelParmMVDataSource")

        first_source = ET.SubElement(source, "Source")
        first_source.text = self.country

        variable = ET.SubElement(source, "Variable")
        variable.set("Ref", "Combined TCC Dimension")

        names = ET.SubElement(source, "Names")
        names.text = "Strings"

        joint_dist = ET.SubElement(source, "JointDist")
        joint_dist.set("Ref", "Combined TCC Dimension")

        min_count = ET.SubElement(source, "MinCount")
        min_count.text = "0"

        views = ET.SubElement(report_def, "Views")

        view = ET.SubElement(views, "View")
        view.set("xsi:type", "DataPointMVView")

        sort = ET.SubElement(view, "Sort")
        sort.text = "Alphabetic"

        reverse = ET.SubElement(view, "Reverse")
        reverse.text = "false"

        display_views = ET.SubElement(view, "DisplayViews")
        display_views.text = "false"

        row_count = ET.SubElement(view, "RowCount")
        row_count.text = "0"
        lower_view = ET.SubElement(view, "View")
        lower_view.text = "None"

        first_dimension = ET.SubElement(root, "Dim1File")
        first_dimension.text = "&& ALL"

        second_dimension = ET.SubElement(root, "Dim2File")
        second_dimension.text = '&& ALL'

        part_time = ET.SubElement(root, "PartTime")
        part_time.text = "false"

        unique = ET.SubElement(root, 'Unique')
        unique.text = 'true'

        no_profile_list = ET.SubElement(root, 'NoProfileLists')
        no_profile_list.text = 'true'

        pfgid = ET.SubElement(root, 'PFGID')
        pfgid.text = "false"

        show_report_error = ET.SubElement(root, 'ShowReportErrors')
        show_report_error.text = 'false'

        currency = ET.SubElement(root, 'Currency')
        currency.text = 'U.S. Dollar (USD)'

        min_date = ET.SubElement(root, 'MinDate')
        min_date.text = self.min_date

        max_date = ET.SubElement(root, 'MaxDate')
        max_date.text = self.max_date

        last_run = ET.SubElement(root, 'LastRunDate')
        last_run.text = str(df.DateTimeFormats().return_today_as_y_m_d("-")) + "T00:00:00"

        exp_date = ET.SubElement(root, 'ExpirationDate')
        exp_date.text = str(df.DateTimeFormats().return_today_as_y_m_d("-")) + "T00:00:00"

        max_results = ET.SubElement(root, 'MaxResults')
        max_results.text = '1000000'

        alt_search = ET.SubElement(root, 'AltSearchMode')
        alt_search.text = ""

        tree = ET.ElementTree(root)
        tree.write(self.output_file, "utf-8", "1.0")


class BuildCountTableXML:

    def __init__(self, index_server,
                 input_file,
                 min_date,
                 max_date,
                 output_file,
                 main_filter="",
                 report_definition="CountTableDefinition",
                 report_measure="Job Title Dimension",
                 ranges="Fixed",
                 sub_filter="UnconfirmedOnly",
                 row_count="0",
                 min_per_row="5",
                 first_dimension_list=None,
                 second_dimension_list=None,
                 first_dimension_file=None,
                 second_dimension_file=None,
                 part_time='true',
                 pfgid='false'):

        self.min_date = min_date + "T00:00:00"
        self.max_date = max_date + "T00:00:00"
        self.output_file = output_file
        self.index_server = index_server
        self.input_file = input_file
        self.main_filter = main_filter
        self.report_definition = report_definition
        self.report_measure = report_measure
        self.ranges = ranges
        self.sub_filter = sub_filter
        self.row_count = row_count
        self.min_per_row = min_per_row
        self.first_dimension_file = first_dimension_file
        self.second_dimension_file = second_dimension_file
        self.first_dimension_list = first_dimension_list
        self.second_dimension_list = second_dimension_list
        self.part_time = part_time
        self.pfgid = pfgid

    def build_count_table_counts_file(self):

        root = ET.Element("AnalysisConfig")
        root.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
        root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

        index_server = ET.SubElement(root, 'IndexServer')
        index_server.text = self.index_server

        name = ET.SubElement(root, 'Name')
        name.text = self.input_file

        text_filter = ET.SubElement(root, 'Filter')
        text_filter.text = self.main_filter

        report_def = ET.SubElement(root, 'ReportDef')
        report_def.set('xsi:type', self.report_definition)

        dimension = ET.SubElement(report_def, 'Dimension')
        under_dimension = ET.SubElement(dimension, 'Dimension')
        under_dimension.set('Ref', self.report_measure)

        ranges = ET.SubElement(dimension, "Ranges")
        ranges.text = self.ranges

        sub_filter = ET.SubElement(dimension, 'Filter')
        sub_filter.text = self.sub_filter

        row_count = ET.SubElement(dimension, 'RowCount')
        row_count.text = self.row_count

        min_per_row = ET.SubElement(dimension, 'MinPerRow')
        min_per_row.text = self.min_per_row

        include_profile_answer = ET.SubElement(report_def, 'IncludeProfileAnswer')
        include_profile_answer.text = "false"

        if self.first_dimension_file is None:
            dim_1_list = ET.SubElement(root, 'Dim1List')
            self.dimension_list_build(dim_1_list, 1)
        else:
            dim_1_file = ET.SubElement(root, 'Dim1File')
            dim_1_file.text = self.first_dimension_file

        if self.second_dimension_file is None:
            dim_2_list = ET.SubElement(root, 'Dim2List')
            self.dimension_list_build(dim_2_list, 2)
        else:
            dim_2_file = ET.SubElement(root, 'Dim2File')
            dim_2_file.text = self.second_dimension_file

        part_time = ET.SubElement(root, 'PartTime')
        part_time.text = self.part_time

        unique = ET.SubElement(root, 'Unique')
        unique.text = 'true'

        no_profile_list = ET.SubElement(root, 'NoProfileLists')
        no_profile_list.text = 'true'

        pfgid = ET.SubElement(root, 'PFGID')
        pfgid.text = self.pfgid

        show_report_error = ET.SubElement(root, 'ShowReportErrors')
        show_report_error.text = 'false'

        currency = ET.SubElement(root, 'Currency')
        currency.text = 'U.S. Dollar (USD)'

        min_date = ET.SubElement(root, 'MinDate')
        min_date.text = self.min_date

        max_date = ET.SubElement(root, 'MaxDate')
        max_date.text = self.max_date

        last_run = ET.SubElement(root, 'LastRunDate')
        last_run.text = str(df.DateTimeFormats().return_today_as_y_m_d("-")) + "T00:00:00"

        exp_date = ET.SubElement(root, 'ExpirationDate')
        exp_date.text = str(df.DateTimeFormats().return_today_as_y_m_d("-")) + "T00:00:00"

        max_results = ET.SubElement(root, 'MaxResults')
        max_results.text = '1000000'

        alt_search = ET.SubElement(root, 'AltSearchMode')
        alt_search.text = ""

        tree = ET.ElementTree(root)
        tree.write(self.output_file, "utf-8", "1.0")

    def dimension_list_build(self, dimension_list, number_of_list):

        if number_of_list == 1:
            file_to_use = self.first_dimension_list
        else:
            file_to_use = self.second_dimension_list

        if file_to_use is None or file_to_use is "":
            string = ET.SubElement(dimension_list, 'string')
            string.text = "AS[.]ALL"
            #as future reference the AS[.]ALL dimension file equivalent
            #is "&amp;&amp; ALL" in case you want to go that direction

        else:
            self.build_quick_dimension_lists(file_to_use, dimension_list)

    def build_quick_dimension_lists(self, file_to_use, dimension_list):

        #assert os.path.isfile(file_to_use) is True, "For Dimension lists you need to give the Build OverTableXml " \
        #                                            "class a file. This is not a file: " + file_to_use

        if "Current Jobs" in file_to_use:
            self.create_job_answer_values(file_to_use, dimension_list)

        elif "Current Rollups" in file_to_use:
            self.create_rollup_answer_values(file_to_use, dimension_list)

        elif "Current Jobs Test.csv" in file_to_use:
            #obviously just used for testing
            #This test file only has two jobs in it so I could get results
            #back very fast
            self.create_job_answer_values(file_to_use, dimension_list)

        elif "Survey PayScale Main" in file_to_use:
            self.create_survey_dimension(dimension_list)
        elif isinstance(file_to_use, list) and file_to_use[0] == 'Certifications/Certifications':
            self.mobile_survey_list_create(dimension_list, file_to_use)

        elif "Country Dimension.csv" in file_to_use:
            try:
                with open(automated_dashboard_path + file_to_use, 'rb') as R:
                    reader = csv.reader(R, delimiter=',')

                    names = reader.next()

                    for row in reader:
                        answer_string = row[names.index('Answer Value')].strip()
                        string = ET.SubElement(dimension_list, 'string')
                        string.text = answer_string

            except IOError:
                print "Couldn't open your file " + file_to_use

        elif "US and Canada" in file_to_use:
            string = ET.SubElement(dimension_list, 'string')
            string.text = "AS[.]AV{Location\Country\United States}"
            string = ET.SubElement(dimension_list, 'string')
            string.text = "AS[.]AV{Location\Country\Canada}"

    @staticmethod
    def mobile_survey_list_create(dimension_list, file_to_use):

        for question in file_to_use:
            split = question.partition("/")
            fore = split[0]
            aft = split[2]
            answer_string = "AS[" + aft + "]ANY{" + fore + "\\" + aft + "}"
            string = ET.SubElement(dimension_list, 'string')
            string.text = answer_string

    @staticmethod
    def create_survey_dimension(dimension_list):

        string = ET.SubElement(dimension_list, 'string')
        string.text = "AS[PayScale Main]AV{Survey\Survey\PayScale Main}"

    @staticmethod
    def create_rollup_answer_values(file_to_use, dimension_list):

        try:
            rollups = []
            with open(automated_dashboard_path + file_to_use, 'rb') as R:
                reader = csv.reader(R, delimiter=',')

                names = reader.next()

                for row in reader:
                    rollup_title = row[names.index('Read-only Answervalue')].strip()
                    if rollup_title != "":
                        rollups.append(rollup_title)

                rollups = list(set(rollups))

                for rollup in rollups:
                    answer_string = "AS[" + rollup + "]AV{Job\\Job.Rollup\\" + rollup + "}"
                    string = ET.SubElement(dimension_list, 'string')
                    string.text = answer_string

        except IOError:
            print "Couldn't open your file " + file_to_use

    @staticmethod
    def create_job_answer_values(file_to_use, dimension_list):

        try:
            with open(automated_dashboard_path + file_to_use, 'rb') as R:
                reader = csv.reader(R, delimiter=',')

                names = reader.next()

                for row in reader:
                    answer_string = row[names.index('ANSWER VALUE')].strip()
                    answer_string = "AS[" + answer_string + "]AV{Job\\Job\\" + answer_string + "}"
                    string = ET.SubElement(dimension_list, 'string')
                    string.text = answer_string

        except IOError:
            print "Couldn't open your file " + file_to_use

    @staticmethod
    def create_question_answer_values(file_to_use, dimension_list):

        try:
            with open(file_to_use, 'rb') as R:
                reader = csv.reader(R, delimiter=',')

                for row in reader:
                    if "All Questions" not in row[0]:
                        answer_string = "AS[" + row[0] + "]ANY{" + row[0].replace("/", "\\") + "}"
                        string = ET.SubElement(dimension_list, 'string')
                        string.text = answer_string
        except IOError:
            print "Couldn't open your file " + file_to_use
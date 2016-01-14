from RequestService import admin_requests as request_data
import serialize_xml as build_xml


class AnonReports:

    def __init__(self, temp_in_files, temp_out_files, ui_update=None):
        """
        :param temp_in_files:
            File path for the Analysis Config Files to be stored
        :param temp_out_files:
            File path for the XML Analysis Tool output to be stored.
        """
        self.temp_in_files = temp_in_files
        self.temp_out_files = temp_out_files
        self.ui_update = ui_update

    def post_analysis_tool_query_pre_made_file_dims(self, index_server,
                                                    in_file,
                                                    start_date,
                                                    end_date,
                                                    main_filter,
                                                    report_measure,
                                                    return_type,
                                                    first_dimension_file=None,
                                                    second_dimension_file=None,
                                                    dimension=None,
                                                    ranges="Fixed",
                                                    confirmed="ConfirmedOnly",
                                                    row_count="0",
                                                    min_per_row="0",
                                                    fitting="Data",
                                                    part_time="True",
                                                    pfgid="False",
                                                    custom_dimension_tuple=None
                                                    ):
        """
        :param index_server:
            Specify which machine you want the report to point at.
        :param in_file:
            name of the analysis tool query you want to run
        :param start_date:
        :param end_date:
        :param main_filter:
            Main Filter on the landing page of the Analysis Tool
        :param report_measure:
            EAC Measure, Profile Age Measure, etc.
        :param return_type:
            The columns drop down in the analysis tool (count, median, medians, etc)
        :param first_dimension_file:
            pre-made dimension file
        :param second_dimension_file:
            pre-made dimension file

        :return:
            Outputs a zipped xml file to self.temp_out_files
        """

        if dimension is None:
            build_xml.BuildOverallTableXML(index_server,
                                           in_file,
                                           start_date,
                                           end_date,
                                           self.temp_in_files + in_file + ".ac.txt",
                                           main_filter=main_filter,
                                           report_measure=report_measure,
                                           return_type=return_type,
                                           report_definition="OverallTableDefinition",
                                           first_dimension_file=first_dimension_file,
                                           second_dimension_file=second_dimension_file,
                                           fitting=fitting,
                                           ).build_overall_table_counts_file()

        else:
            build_xml.BuildOverallTableXML(index_server,
                                           in_file,
                                           start_date,
                                           end_date,
                                           self.temp_in_files + in_file + ".ac.txt",
                                           main_filter=main_filter,
                                           report_measure=report_measure,
                                           return_type=return_type,
                                           report_definition="TableDefinition",
                                           first_dimension_file=first_dimension_file,
                                           second_dimension_file=second_dimension_file,
                                           dimension=dimension,
                                           ranges=ranges,
                                           confirmed=confirmed,
                                           row_count=row_count,
                                           min_per_row=min_per_row,
                                           custom_dimension_tuple=custom_dimension_tuple
                                           ).build_overall_table_counts_file()

        request_data.PostToAnalysisTool(self.temp_in_files + in_file + ".ac.txt",
                                        self.temp_out_files + in_file + ".zip",
                                        self.ui_update).run()

    def post_analysis_tool_query_dim_list_create(self,
                                                 index_server,
                                                 in_file,
                                                 start_date,
                                                 end_date,
                                                 main_filter,
                                                 report_measure,
                                                 return_type,
                                                 first_dimension_list=None,
                                                 second_dimension_list=None,
                                                 dimension=None,
                                                 ranges="Fixed",
                                                 confirmed="ConfirmedOnly",
                                                 row_count="0",
                                                 min_per_row="0",
                                                 fitting="Data",
                                                 part_time="True",
                                                 pfgid="False",
                                                 string_builder_type=None
                                                 ):
        """
        :param index_server:
            Specify which machine you want the report to point at.
        :param in_file:
            name of the analysis tool query you want to run
        :param start_date:
        :param end_date:
        :param main_filter:
            Main Filter on the landing page of the Analysis Tool
        :param report_measure:
            EAC Measure, Profile Age Measure, etc.
        :param return_type:
            The columns drop down in the analysis tool (count, median, medians, etc)
        :param first_dimension_list:
            dimension file you want created. Should be pointed to a csv file.
        :param second_dimension_list:
            dimension file you want created. Should be pointed to a csv file.

        :return:
            Outputs a zipped xml file to self.temp_out_files
        """
        if dimension is None:
            build_xml.BuildOverallTableXML(index_server,
                                           in_file,
                                           start_date,
                                           end_date,
                                           self.temp_in_files + in_file + ".ac.txt",
                                           main_filter=main_filter,
                                           report_measure=report_measure,
                                           return_type=return_type,
                                           report_definition="OverallTableDefinition",
                                           first_dimension_list=first_dimension_list,
                                           second_dimension_list=second_dimension_list,
                                           fitting=fitting,
                                           string_builder_type=string_builder_type
                                           ).build_overall_table_counts_file()

        else:
            build_xml.BuildOverallTableXML(index_server,
                                           in_file,
                                           start_date,
                                           end_date,
                                           self.temp_in_files + in_file + ".ac.txt",
                                           main_filter=main_filter,
                                           report_measure=report_measure,
                                           return_type=return_type,
                                           report_definition="TableDefinition",
                                           first_dimension_list=first_dimension_list,
                                           second_dimension_list=second_dimension_list,
                                           dimension=dimension,
                                           ranges=ranges,
                                           confirmed=confirmed,
                                           row_count=row_count,
                                           min_per_row=min_per_row,
                                           string_builder_type=string_builder_type
                                           ).build_overall_table_counts_file()

        request_data.PostToAnalysisTool(self.temp_in_files + in_file + ".ac.txt",
                                        self.temp_out_files + in_file + ".zip").run()

    def post_analysis_tool_model_report(self,
                                        index_server,
                                        input_file,
                                        country):

        build_xml.BuildMVariateViewDefinition(index_server,
                                              input_file,
                                              self.temp_in_files + input_file + ".ac.txt",
                                              country).build_xml_file()

        request_data.PostToAnalysisTool(self.temp_in_files + input_file + ".ac.txt",
                                        self.temp_out_files + input_file + ".zip").run()

    def post_analysis_tool_count_table_report(self,
                                              index_server,
                                              in_file,
                                              start_date,
                                              end_date,
                                              main_filter,
                                              first_dimension_list=None,
                                              second_dimension_list=None,
                                              first_dimension_file=None,
                                              second_dimension_file=None,
                                              custom_dimension_tuple=None,
                                              report_definition=None,
                                              sub_filter='UnconfirmedOnly',
                                              min_per_row='0',
                                              profile_count=None,
                                              sampling_method=None,
                                              group_by_first_dim=None,
                                              row_names=None,
                                              add_dim_definition=None):


        build_xml.BuildCountTableXML(index_server,
                                     in_file,
                                     start_date,
                                     end_date,
                                     self.temp_in_files + in_file + ".ac.txt",
                                     main_filter=main_filter,
                                     first_dimension_list=first_dimension_list,
                                     second_dimension_list=second_dimension_list,
                                     first_dimension_file=first_dimension_file,
                                     second_dimension_file=second_dimension_file,
                                     custom_dimension_tuple=custom_dimension_tuple,
                                     report_definition=report_definition,
                                     sub_filter=sub_filter,
                                     min_per_row=min_per_row,
                                     profile_count=profile_count,
                                     sampling_method=sampling_method,
                                     group_by_first_dim=group_by_first_dim,
                                     row_names=row_names,
                                     add_dim_definition=add_dim_definition
                                     ).build_count_table_counts_file()

        request_data.PostToAnalysisTool(self.temp_in_files + in_file + ".ac.txt",
                                        self.temp_out_files + in_file + ".zip",
                                        self.ui_update).run()


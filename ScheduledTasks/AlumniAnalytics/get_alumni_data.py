from PyQt4 import QtCore
import AnalysisTool.deserialize_xml as my_xml
import RyanBot.DataDashboard.dashboard_support as ds
dash = ds.DashboardSupport()
import AnalysisTool.extract_data_xml as extract
import Constants.constant_strings as cs
const = cs.Constants()
import DateFunctions.datetimes_in as dat
dates = dat.DateTimeFormats()
import AnalysisTool.run_queries as rq
import datetime
import os
import csv

report_measure = 'EAC Measure'
return_type = 'Medians'
ranges = 'Fixed'


file_dimension = {1: 'Alumni Analytics File Dimension 1',
                  2: 'Alumni Analytics EducationalLevelAffiliateSchool', 3: 'Alumni Analytics File Dimension YG',
                  4: '&& ALL', 5: '&& ALL'}

table_dimension = {1: 'Alumni Analytics Table Dimension 1',
                   2: 'Alumni Analytics Table Dimension Jobs', 3: 'Alumni Analytics Table Dimension YG',
                   4: 'Alumni Analytics Schools', 5: '&& ALL'}

main_dimension = {1: ('school', 'educationallevelaffiliateschool'),
                  2: 'ONET 30 Dimension', 3: ('school', 'educationallevelaffiliateschool'),
                  4: ('school', 'educationallevelaffiliateschool'), 5: ('educationvalue', 'commentbox')}

min_per_row = {1: '0', 2: '0', 3: '0', 4: '3', 5:'0'}


class AlumniDTO:

    def __init__(self):
        self.query_01 = {}
        self.query_02 = {}
        self.query_03 = {}
        self.query_04 = {}
        self.query_05 = {}
        self.query_06 = {}


class AlumniDataCollect(QtCore.QThread):

    update_string_progress = QtCore.pyqtSignal(str)

    def __int__(self):
        QtCore.QThread.__init__(self)
        self.start_date = None
        self.end_date = None
        self.query_base_name = None
        self.main_filter = None
        self.affiliate_id = None
        self.DTO = AlumniDTO()

    def get_date(self, target_date, start = True):
        if start:
            self.start_date = target_date.date().toPyDate().strftime("%Y-%m-%d")
        else:
            self.end_date = target_date.date().toPyDate().strftime("%Y-%m-%d")

    def set_main_filter(self, affiliate_id):
        if affiliate_id is not None:
            self.main_filter = r'Location\Country\United States{match,1,0} & profile\affiliate{IRange,3,0,%s,%s}' \
                               % (affiliate_id, affiliate_id)
            self.affiliate_id = affiliate_id

    def set_base_name(self, base_name):
        self.query_base_name = base_name

    def test_dates(self):
        start_year, start_month, start_day = self.start_date.split('-')
        start_date = datetime.datetime(int(start_year), int(start_month), int(start_day))

        end_year, end_month, end_day = self.end_date.split('-')
        end_date = datetime.datetime(int(end_year), int(end_month), int(end_day))

        if start_date >= end_date:
            self.update_string_progress.emit("The end date must be greater than the start date")
            return False
        else:
            return True

    def run(self):
        if self.test_parameters() and self.test_dates():
            self.fire_queries()
            self.gather_results()
            self.file_writing()
            self.clean_up_results()
            self.update_string_progress.emit("All finished, son!")

    def test_parameters(self):
        if self.affiliate_id is '':
            self.update_string_progress.emit("Please enter a value for affiliate id")
            return False
        else:
            return True

    def unzip_results(self):
        for zip_files in os.listdir(const.anon_out):
            if ".zip" in zip_files and 'Gina Alumni Analytics' in zip_files:
                dash.unzip_file(zip_files, const.anon_out)

    def file_writing(self):
        fifth_header = ['Config', 'File', 'Table', 'Row', 'Count', 'Percent']
        sixth_header = ['Config', 'File', 'Table', 'Row', 'PID', 'educationvalue\commentbox']
        self.write_to_file('Gina %s Query 01' % self.affiliate_id, self.DTO.query_01)
        self.write_to_file('Gina %s Query 02' % self.affiliate_id, self.DTO.query_02)
        self.write_to_file('Gina %s Query 03' % self.affiliate_id, self.DTO.query_03)
        self.write_to_file('Gina %s Query 04' % self.affiliate_id, self.DTO.query_04)
        self.write_fifth_sixth_to_file('Gina %s Query 05' % self.affiliate_id, self.DTO.query_05, fifth_header)
        self.write_fifth_sixth_to_file('Gina %s Query 06' % self.affiliate_id, self.DTO.query_06, fifth_header)

    def write_to_file(self, file_name, dict_to_use):
        self.update_string_progress.emit("Writing %s... " % (file_name))
        with open(const.alumni_analytics + file_name + '.csv', 'wb') as W:
            writer = csv.writer(W, delimiter=',', lineterminator='\n')

            header = ['Config', 'File', 'Table', 'Row', 'Count', 'Percent', '10%', '25%', '50%', '75%', '90%']
            writer.writerow(header)

            for main_key in dict_to_use:
                for file_line in dict_to_use[main_key]:
                    for table_line in dict_to_use[main_key][file_line]:
                        for row in dict_to_use[main_key][file_line][table_line]:
                            length = 0
                            final_line = [main_key, file_line, table_line, row]
                            for items in dict_to_use[main_key][file_line][table_line][row]:
                                eac_list = dict_to_use[main_key][file_line][table_line][row]
                                if items == 'NaN':
                                    items = ''
                                final_line.append(items)
                                length += 1
                                if length == len(eac_list):
                                    writer.writerow(final_line)

    def write_fifth_sixth_to_file(self, file_name, dict_to_use, header):
        self.update_string_progress.emit("Writing %s... " % file_name)
        with open(const.alumni_analytics + file_name + '.csv', 'wb') as W:
            writer = csv.writer(W, delimiter=',', lineterminator='\n')
            writer.writerow(header)

            for main_key in dict_to_use:
                for file_line in dict_to_use[main_key]:
                    for table_line in dict_to_use[main_key][file_line]:
                        for row in dict_to_use[main_key][file_line][table_line]:
                            length = 0
                            final_line = [main_key, file_line, table_line, row]
                            for items in dict_to_use[main_key][file_line][table_line][row]:
                                eac_list = dict_to_use[main_key][file_line][table_line][row]
                                if items == 'NaN':
                                    items = ''
                                final_line.append(items)
                                length += 1
                                if length == len(eac_list):
                                    writer.writerow(final_line)

    def gather_results(self):
        self.DTO = AlumniDTO()
        for xml_files in os.listdir(const.anon_out):
            if ".xml" in xml_files and 'Gina Alumni Analytics' in xml_files:
                my_xml.fix_xml_encoding(const.anon_out, xml_files)

            if 'Gina Alumni Analytics Query 1' in xml_files and '.xml' in xml_files:
                self.update_string_progress.emit("Pulling from %s... " % (xml_files))
                data_dict = extract.ExtractXMLData(const.anon_out + xml_files).table_def_medians_list_handler()
                main_key = 'Gina %s Query 01' % self.affiliate_id
                self.update_dictionaries(xml_files, main_key, data_dict, self.DTO.query_01)

            elif 'Gina Alumni Analytics Query Large' in xml_files and '.xml' in xml_files:
                self.update_string_progress.emit("Pulling from %s... " % (xml_files))
                data_dict = extract.ExtractXMLData(const.anon_out + xml_files).table_def_medians_list_handler()
                main_key = 'Gina %s Query 02' % self.affiliate_id
                self.update_dictionaries(xml_files, main_key, data_dict, self.DTO.query_02)

            elif 'Gina Alumni Analytics Query 2' in xml_files and '.xml' in xml_files:
                self.update_string_progress.emit("Pulling from %s... " % (xml_files))
                data_dict = extract.ExtractXMLData(const.anon_out + xml_files).table_def_medians_list_handler()
                main_key = 'Gina %s Query 03' % self.affiliate_id
                self.update_dictionaries(xml_files, main_key, data_dict, self.DTO.query_03)

            elif 'Gina Alumni Analytics Query 3' in xml_files and '.xml' in xml_files:
                self.update_string_progress.emit("Pulling from %s... " % (xml_files))
                data_dict = extract.ExtractXMLData(const.anon_out + xml_files).table_def_medians_list_handler()
                main_key = 'Gina %s Query 04' % self.affiliate_id
                self.update_dictionaries(xml_files, main_key, data_dict, self.DTO.query_04)

            elif 'Gina Alumni Analytics Query 4' in xml_files and '.xml' in xml_files:
                self.update_string_progress.emit("Pulling from %s... " % (xml_files))
                data_dict = extract.ExtractXMLData(const.anon_out + xml_files).table_def_medians_list_handler()
                main_key = 'Gina %s Query 05' % self.affiliate_id
                self.update_dictionaries(xml_files, main_key, data_dict, self.DTO.query_05)

            elif 'Gina Alumni Analytics Query 5' in xml_files and '.xml' in xml_files:
                self.update_string_progress.emit("Pulling from %s... " % (xml_files))
                data_dict = extract.ExtractXMLData(const.anon_out + xml_files).sample_def_alumni_analytics_handler()
                main_key = 'Gina %s Query 06' % self.affiliate_id
                self.update_dictionaries(xml_files, main_key, data_dict, self.DTO.query_06)

    def update_dictionaries(self, xml_files, main_key, data_dict, target_dict):
            self.update_string_progress.emit("Pulling from %s... " % (xml_files))
            if main_key not in self.DTO.query_01.keys():
                self.DTO.query_01[main_key] = data_dict
            else:
                copy_dict = self.DTO.query_01[main_key]
                copy_dict.update(data_dict)
                self.DTO.query_01[main_key] = copy_dict

    def clean_up_results(self):
        for old_files in os.listdir(const.anon_out):
            if ('.xml' in old_files) and 'Gina Alumni Analytics' in old_files:
                os.remove(const.anon_out + old_files)


    def fire_queries(self):
        anon = rq.AnonReports(const.anon_in, const.anon_out, self.update_string_progress)
        #alumni_files = os.listdir(const.alumni_analytics_in)

        for x in xrange(1, 11):
            self.update_string_progress.emit("Starting %s... " % (self.query_base_name + 'Large' + str(x)))
            dimension_to_use = 'Custom'
            anon.post_analysis_tool_query_pre_made_file_dims('localhost',
                                                             self.query_base_name + 'Large ' + str(x),
                                                             self.start_date,
                                                             self.end_date,
                                                             self.main_filter,
                                                             report_measure,
                                                             return_type,
                                                              'Alumni Analytics File Dimension Majors',
                                                             'Alumni Analytics Major Dimension %s' % x,
                                                             dimension=dimension_to_use,
                                                             ranges=ranges,
                                                             custom_dimension_tuple=('school',
                                                                                     'educationallevelaffiliateschool'),
                                                             min_per_row='0'
                                                             )

        #for i in xrange(1, 6):
        for i in xrange(2, 4):
            custom = None
            dimension_to_use = None
            if type(main_dimension[i]) is tuple:
                custom = main_dimension[i]
                dimension_to_use = 'Custom'
            else:
                custom = None
                dimension_to_use = main_dimension[i]
            self.update_string_progress.emit("Starting %s... " % (self.query_base_name + str(i)))
            if i < 4:
                anon.post_analysis_tool_query_pre_made_file_dims('localhost',
                                                                 self.query_base_name + str(i),
                                                                 self.start_date,
                                                                 self.end_date,
                                                                 self.main_filter,
                                                                 report_measure,
                                                                 return_type,
                                                                 file_dimension[i],
                                                                 table_dimension[i],
                                                                 dimension=dimension_to_use,
                                                                 ranges=ranges,
                                                                 custom_dimension_tuple=custom,
                                                                 min_per_row=min_per_row[i]
                                                                 )

            else:
                report_setting = None
                sub_filter = 'ConfirmedOnly'

                if i == 4:
                    report_setting = 'CountTableDefinition'
                    sample_measures = [None, None, None, None, None]
                else:
                    report_setting = 'SampleDefinition'
                    sample_measures = ['1000', 'Top', 'false', 'ProfileID', 'false']

                anon.post_analysis_tool_count_table_report('localhost',
                                                           self.query_base_name + str(i),
                                                           self.start_date,
                                                           self.end_date,
                                                           self.main_filter,
                                                           first_dimension_file=file_dimension[i],
                                                           second_dimension_file=table_dimension[i],
                                                           custom_dimension_tuple=main_dimension[i],
                                                           report_definition=report_setting,
                                                           sub_filter=sub_filter,
                                                           min_per_row=min_per_row[i],
                                                           profile_count=sample_measures[0],
                                                           sampling_method=sample_measures[1],
                                                           group_by_first_dim=sample_measures[2],
                                                           row_names=sample_measures[3],
                                                           add_dim_definition=sample_measures[4]
                                                           )



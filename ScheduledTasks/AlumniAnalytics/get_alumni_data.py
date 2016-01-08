from PyQt4 import QtCore
import RyanBot.DataDashboard.dashboard_support as ds
dash = ds.DashboardSupport()
import Constants.constant_strings as cs
const = cs.Constants()
import DateFunctions.datetimes_in as dat
dates = dat.DateTimeFormats()
import AnalysisTool.run_queries as rq
import datetime
import os

report_measure = 'EAC Measure'
return_type = 'Medians'
ranges = 'Fixed'


file_dimension = {1: 'Alumni Analytics File Dimension 1', #2: 'Alumni Analytics File Dimension Majors',
                  2: 'Alumni Analytics EducationalLevelAffiliateSchool', 3: 'Alumni Analytics File Dimension YG',
                  4: '&&ALL', 5: '&&ALL'}

table_dimension = {1: 'Alumni Analytics Table Dimension 1', #2: 'Alumni Analytics Major Dimension Testing Ginge',
                   2: 'Alumni Analytics Table Dimension Jobs', 3: 'Alumni Analytics Table Dimension YG',
                   4: 'Alumni Analytics Schools', 5: '&&ALL'}

main_dimension = {1: ('school', 'educationallevelaffiliateschool'), #2: ('school', 'educationallevelaffiliateschool'),
                  2: 'ONET 30 Dimension', 3: ('school', 'educationallevelaffiliateschool'),
                  4: ('school', 'educationallevelaffiliateschool'), 5: ('educationvalue', 'commentbox')}

min_per_row = {1: '0', 2: '0', 3: '0', 4: '3', 5:'3'}


class AlumniDataCollect(QtCore.QThread):

    update_string_progress = QtCore.pyqtSignal(str)

    def __int__(self):
        QtCore.QThread.__init__(self)
        self.start_date = None
        self.end_date = None
        self.query_base_name = None
        self.main_filter = None
        self.affiliate_id = None

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

    def test_parameters(self):
        if self.affiliate_id is '':
            self.update_string_progress.emit("Please enter a value for affiliate id")
            return False
        else:
            return True


    def fire_queries(self):
        anon = rq.AnonReports(const.anon_in, const.anon_out, self.update_string_progress)
        alumni_files = os.listdir(const.alumni_analytics_in)
        for x in xrange(1, 11):
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

        for i in xrange(1, 6):
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
                '''
            else:
                report_setting = None
                sub_filter = 'ConfirmedOnly'

                if i == 4:
                    report_setting = 'CountTableDefinition'
                else:
                    report_setting = 'SampleDefinition'

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
                                                           min_per_row=min_per_row
                                                           )
                '''
import AnalysisTool.deserialize_xml as my_xml
import os
import AnalysisTool.run_queries as rq
import RyanBot.DataDashboard.dashboard_support as ds
dash = ds.DashboardSupport()
import Constants.constant_strings as cs
const = cs.Constants()
import DateFunctions.datetimes_in as dat
dates = dat.DateTimeFormats()
import csv


#---------------------#
#All report Definitions
#---------------------#
profiles_by_type = 'Rachel Data Dashboard Active Profiles by Type'
all_profiles_by_type = 'Rachel Data Dashboard All Profiles by Type'
current_profile_counts = 'Rachel Data Dashboard Current Profile Counts'
last_month_start = dates.return_ymd_first_of_last_month('-')
last_month_end = dates.find_first_of_current_month('-')
#last_month_start = '2015-10-01'
#last_month_end = '2015-11-01'
main_filter = ''
report_measure = 'Profile Age Measure'
return_type = 'Count'
file_dimension = 'ProfileTypes BreakDown'
table_dimension = 'Country Canada & US and ALL'
dimension = 'Profile Age Dimension'
ranges = 'Singleton'
file_write_name = 'Profile counts by Type.csv'

all_key = 'All'
us_ca = 'US & CA'


#DTO
class ProfileCounts:
    def __int__(self):
        self.job_offer = {}
        self.current_job = {}
        self.alumni = {}
        self.informational = {}


active_profiles = ProfileCounts()
all_profiles = ProfileCounts()

#-------------------------#
#Let's fire this thing off#
#-------------------------#

anon = rq.AnonReports(const.anon_in, const.anon_out)
anon.post_analysis_tool_query_pre_made_file_dims('localhost',
                                                 profiles_by_type,
                                                 last_month_start,
                                                 last_month_end,
                                                 main_filter,
                                                 report_measure,
                                                 return_type,
                                                 file_dimension,
                                                 table_dimension,
                                                 dimension=dimension,
                                                 ranges=ranges,
                                                 )

anon.post_analysis_tool_query_pre_made_file_dims('psbuilder02a',
                                                 all_profiles_by_type,
                                                 last_month_start,
                                                 last_month_end,
                                                 main_filter,
                                                 report_measure,
                                                 return_type,
                                                 file_dimension,
                                                 table_dimension,
                                                 dimension=dimension,
                                                 ranges=ranges,
                                                 )
'''
anon.post_analysis_tool_query_pre_made_file_dims('psbuilder01a',
                                                 current_profile_counts,
                                                 last_month_start,
                                                 last_month_end,
                                                 main_filter,
                                                 report_measure,
                                                 return_type,
                                                 '&& ALL',
                                                 table_dimension,
                                                 dimension=None,
                                                 ranges=ranges)

#Open up all the zipped presents!!!
for zip_files in os.listdir(const.anon_out):
    if ".zip" in zip_files and 'Rachel' in zip_files:
        dash.unzip_file(zip_files, const.anon_out)

#Put that fanciness in a DTO!!!
for xml_files in os.listdir(const.anon_out):
    if ".xml" in xml_files:
        my_xml.fix_xml_encoding(const.anon_out, xml_files)
'''
'''
        if 'All Profiles' in xml_files and 'Rachel Data Dashboard' in xml_files:
            if '_0' in xml_files:
                all_profiles.job_offer = dash.pull_job_data_from_xml(const.anon_out + xml_files)
            elif '_1' in xml_files:
                all_profiles.current_job = dash.pull_job_data_from_xml(const.anon_out + xml_files)
            elif '_2' in xml_files:
                all_profiles.alumni = dash.pull_job_data_from_xml(const.anon_out + xml_files)
            elif '_3' in xml_files:
                all_profiles.informational = dash.pull_job_data_from_xml(const.anon_out + xml_files)
        elif 'Rachel Data Dashboard' in xml_files and 'Active Profiles' in xml_files:
            if '_0' in xml_files:
                active_profiles.job_offer = dash.pull_job_data_from_xml(const.anon_out + xml_files)
            elif '_1' in xml_files:
                active_profiles.current_job = dash.pull_job_data_from_xml(const.anon_out + xml_files)
            elif '_2' in xml_files:
                active_profiles.alumni = dash.pull_job_data_from_xml(const.anon_out + xml_files)
            elif '_3' in xml_files:
                active_profiles.informational = dash.pull_job_data_from_xml(const.anon_out + xml_files)

#Creating the row of metrics
final_row_list = []

def push_it(item):
    final_row_list.append(item)

def divide_it(num, den):
    try:
        return float(num) / float(den)
    except (ZeroDivisionError):
        return 0
try:
    #Damn, son! So, much to put in the damn file!!!
    push_it(last_month_start)#date
    #Denominators
    push_it(all_profiles.job_offer[all_key])#Total Job Offer Count All
    push_it(all_profiles.job_offer[us_ca])#Total Job Offer Count US & CA
    push_it(all_profiles.job_offer[all_key] - all_profiles.job_offer[us_ca])#Total Job Offer Count Non-US & CA
    push_it(all_profiles.current_job[all_key])#Total Current Job Count All
    push_it(all_profiles.current_job[us_ca])#Total Current Job Count US & CA
    push_it(all_profiles.current_job[all_key] - all_profiles.current_job[us_ca])#Total Current Job Count Non-US & CA
    push_it(all_profiles.informational[all_key])#Total Informational Count All
    push_it(all_profiles.informational[us_ca])#Total Informational Count US & CA
    push_it(all_profiles.informational[all_key] - all_profiles.informational[us_ca])#Total Informational Count Non-US & CA
    push_it(all_profiles.alumni[all_key])#Total Alumni Count All
    push_it(all_profiles.alumni[us_ca])#Total Alumni Count US & CA
    push_it(all_profiles.alumni[all_key] - all_profiles.alumni[us_ca])#Total Alumni Count Non-US & CA

    #Numerators
    push_it(active_profiles.job_offer[all_key])#Active Job Offer Count All
    push_it(active_profiles.job_offer[us_ca])#Active Job Offer Count US & CA
    push_it(active_profiles.job_offer[all_key] - active_profiles.job_offer[us_ca])#Active Job Offer Count Non-US & CA
    push_it(active_profiles.current_job[all_key])#Active Current Job Count All
    push_it(active_profiles.current_job[us_ca])#Active Current Job Count US & CA
    push_it(active_profiles.current_job[all_key] - active_profiles.current_job[us_ca])#Active Current Job Count Non-US & CA
    push_it(active_profiles.alumni[all_key])#Active Alumni Count All
    push_it(active_profiles.alumni[us_ca])#Active Alumni Count US & CA
    push_it(active_profiles.alumni[all_key] - active_profiles.alumni[us_ca])#Active Alumni Count Non-US & CA

    #Metrics
    push_it(divide_it(active_profiles.job_offer[all_key], all_profiles.job_offer[all_key]))#Job Offer Activation Rate All
    push_it(divide_it(active_profiles.job_offer[us_ca], all_profiles.job_offer[us_ca]))#Job Offer Activation Rate US & CA
    job_non_num = active_profiles.job_offer[all_key] - active_profiles.job_offer[us_ca]#Job Offer Activation Rate Non-US & CA
    job_non_den = all_profiles.job_offer[all_key] - all_profiles.job_offer[us_ca]#Job Offer Activation Rate Non-US & CA
    push_it(divide_it(job_non_num, job_non_den))#Job Offer Activation Rate Non-US & CA
    push_it(divide_it(active_profiles.current_job[all_key], all_profiles.current_job[all_key]))#Current Job Activation Rate All
    push_it(divide_it(active_profiles.current_job[us_ca], all_profiles.current_job[us_ca]))#Current Job Activation Rate US & CA
    cur_non_num =  active_profiles.current_job[all_key] - active_profiles.current_job[us_ca]#Current Job Activation Rate Non-US & CA
    cur_non_den = all_profiles.current_job[all_key] - all_profiles.current_job[us_ca]#Current Job Activation Rate Non-US & CA
    push_it(divide_it(cur_non_num, cur_non_den))#Current Job Activation Rate Non-US & CA
    push_it(divide_it(active_profiles.alumni[all_key], all_profiles.alumni[all_key]))#Alumni Activation Rate All
    push_it(divide_it(active_profiles.alumni[us_ca], all_profiles.alumni[us_ca]))#Alumni Activation Rate US & CA
    alum_non_num =  active_profiles.alumni[all_key] - active_profiles.alumni[us_ca]#Alumni Activation Rate Non-US & CA
    alum_non_den = all_profiles.alumni[all_key] - all_profiles.alumni[us_ca]#Alumni Activation Rate Non-US & CA
    push_it(divide_it(alum_non_num, alum_non_den))#Alumni Activation Rate Non-US & CA
except:
    print 'Something went wrong. Most likely the counts for psbuilder02a haven\'t been updated yet.'
    raise SystemExit

#append 1 new row
with open(const.profile_counts + file_write_name, 'ab') as R:
    writer = csv.writer(R, delimiter=',')

    writer.writerow(final_row_list)

#clean up our dirty laundry
for old_files in os.listdir(const.anon_out):
    if ('.zip' in old_files or '.xml' in old_files) and 'Rachel Data Dashboard' in old_files:
        os.remove(const.anon_out + old_files)'''

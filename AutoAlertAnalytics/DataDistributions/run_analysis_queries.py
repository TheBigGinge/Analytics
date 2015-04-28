import data_distributions as data_dist
import DateFunctions.date_functions as dates
import data_dist_database as db

analytics_file_path = '\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\temporary_files\\in_files\\'
#Find the most recent sunday. This is for the week by week data pulls
#since the weeks end on sunday
most_recent_sunday = dates.DateFunctions().find_most_recent_sunday()
most_recent_sunday = dates.DateFunctions().datetime_to_string_y_m_d(most_recent_sunday, "-")


def find_weekly_query_start_date(table):
    last_run_date = db.DatabaseWork().pull_most_recent_date_value(table) + 1
    last_run_date = str(last_run_date)

    year = last_run_date[:4]
    month = last_run_date[4:6]
    day = last_run_date[6:8]

    return year + "-" + month + "-" + day


def find_monthly_query_start_date(table):
    last_run_date = str(db.DatabaseWork().pull_most_recent_date_value(table))

    year = int(last_run_date[:4])
    month = int(last_run_date[4:6]) + 1

    if month == 13:
        month = 1
        year += 1

    month = str(month)

    if len(month) == 1:
        month = "0" + month

    return str(year) + "-" + month + "-" + "01"


def run_weekly_queries():
    """
    Run all the pre-planned weekly analysis tool queries
    """
    '''All Active Profiles'''
    active_start = find_weekly_query_start_date('active_profiles')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Week by Week All Actives",
                                                           active_start,
                                                           most_recent_sunday,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "&& ALL",
                                                           "Date Ranges Weeks 2010 to 2016")
    """Total Profiles"""
    total_start = find_weekly_query_start_date("overall_profiles")
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist Week by Week Total Profiles",
                                                           total_start,
                                                           most_recent_sunday,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "&& ALL",
                                                           "Date Ranges Weeks 2010 to 2016")
    """
    '''Combined Salary'''
    salary_start = find_weekly_query_start_date("combined_salary_weekly")
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Week by Week Combined Salary",
                                                           "Ryan Data Dist Week by Week Combined Salary",
                                                           salary_start,
                                                           most_recent_sunday,
                                                           "",
                                                           "Combined Salary Measure",
                                                           "Medians",
                                                           "&& ALL",
                                                           "Date Ranges Weeks 2010 to 2016")
    '''EAC Medians'''
    eac_start = find_weekly_query_start_date("eac_weekly")
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Week by Week EAC Medians",
                                                           "Ryan Data Dist Week by Week EAC Medians",
                                                           eac_start,
                                                           most_recent_sunday,
                                                           "",
                                                           "EAC Measure",
                                                           "Medians",
                                                           "&& ALL",
                                                           "Date Ranges Weeks 2010 to 2016")
    """

#Find the first day of the current month (in case this is being ran on the 2nd or 3rd)
#This is for the monthly queries

first_of_month = dates.DateFunctions().return_ymd_first_of_the_current_month("-")


def run_monthly_queries():
    """
    Run the monthly pre-planned analysis tool queries.

    These bad boys will take a while since they're going to output all of the data via months
    as dimension files.

    These should be running at night.
    """

    '''Rollups'''
    rollup_start = find_monthly_query_start_date('rollups')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Rollups",
                                                           rollup_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Job Rollup Dimension")

    over_rollup_start = find_monthly_query_start_date('rollups_overall')
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist Rollups Overall",
                                                           over_rollup_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Job Rollup Dimension")

    '''ONET'''
    onet_start = find_monthly_query_start_date('onet_forty')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist ONET 40",
                                                           onet_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="ONET 40 Dimension")

    over_onet_start = find_monthly_query_start_date('onet_forty')
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist ONET 40 Overall",
                                                           over_onet_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="ONET 40 Dimension")

    '''NAICS'''
    naics_start = find_monthly_query_start_date('naics_codes')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Month by Month NAICS 40",
                                                           naics_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Industry 40 Dimension")

    over_naics_start = find_monthly_query_start_date('naics_codes_overall')
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist Month by Month NAICS 40 Overall",
                                                           over_naics_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Industry 40 Dimension")
    '''Metros'''
    metro_start = find_monthly_query_start_date('metro_main')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Metros",
                                                           metro_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Metro Dimension")

    over_metro_start = find_monthly_query_start_date('metro_main_overall')
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist Metros Overall",
                                                           over_metro_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Metro Dimension")
    '''Degree Affinties'''
    degree_start = find_monthly_query_start_date('degree_affinities')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Degree Affinities",
                                                           degree_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Degree Affinity Dimension")

    over_degree_start = find_monthly_query_start_date('degree_affinities_overall')
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist Degree Affinities Overall",
                                                           "Ryan Data Dist Degree Affinities Overall",
                                                           over_degree_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Degree Affinity Dimension")
    '''Company Size'''
    company_start = find_monthly_query_start_date('company_size')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Company Sizes",
                                                           company_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Number Employees Dimension")

    over_company_start = find_monthly_query_start_date('company_size_overall')
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist Company Sizes Overall",
                                                           over_company_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Number Employees Dimension")
    '''AGE'''
    age_start = find_monthly_query_start_date('age_ranges')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist Age Buckets",
                                                           age_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Age Dimension",
                                                           ranges="Dynamic")

    over_age_start = find_monthly_query_start_date('age_ranges_overall')
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist Age Buckets Overall",
                                                           over_age_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Age Dimension",
                                                           ranges="Dynamic")
    '''YE'''
    ye_start = find_monthly_query_start_date('years_experience')
    data_dist.DataDistributions().post_analysis_tool_query("localhost",
                                                           "Ryan Data Dist YE",
                                                           ye_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Experience Dimension")

    over_ye_start = find_monthly_query_start_date('years_experience_overall')
    data_dist.DataDistributions().post_analysis_tool_query("psbuilder02a",
                                                           "Ryan Data Dist YE Overall",
                                                           over_ye_start,
                                                           first_of_month,
                                                           "",
                                                           "Profile Age Measure",
                                                           "Count",
                                                           "Date Ranges Months 2010 to 2017",
                                                           "&& ALL",
                                                           dimension="Experience Dimension")
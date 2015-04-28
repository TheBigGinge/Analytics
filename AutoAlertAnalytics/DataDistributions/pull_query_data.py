import os

import AnalysisTool.deserialize_xml as pull
import data_distributions as dd
import data_dist_database as db


zip_path = "\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\temporary_files\\out_files\\"


def pull_weekly_analysis_tool_data_to_dict(zip_file, medians=False):

    dd.DataDistributions().zip_file_open(zip_file)

    file_name = zip_file[zip_file.rfind("\\") + 1:].strip(".zip")

    for files in os.listdir(dd.DataDistributions().temp_out_files):
        if file_name in files and "_" in files:

            pull.fix_xml_encoding(zip_path, files)

            if medians is True:
                print "Pulling data from " + files + "..."
                weekly_dictionary = dd.DataDistributions().pull_medians_data(files)
            else:
                print "Pulling data from " + files + "..."
                weekly_dictionary = dd.DataDistributions().pull_count_data(files)

            return weekly_dictionary


def pull_monthly_analysis_tool_data_to_dict(zip_file):
    dd.DataDistributions().zip_file_open(zip_file)

    file_name = zip_file[zip_file.rfind("\\") + 1:].strip(".zip")
    monthly_dictionary = {}

    for files in os.listdir(dd.DataDistributions().temp_out_files):
        if file_name in files and "_" in files:
            if "Overall" not in file_name and "Overall" in files:
                continue
            else:
                print "Pulling data from " + files + "..."

                pull.fix_xml_encoding(zip_path, files)

                temporary_dictionary = dd.DataDistributions().pull_monthly_count_data(files)
                monthly_dictionary.update(temporary_dictionary)

    return monthly_dictionary


db.DatabaseWork().update_database_with_weekly_values(
    pull_weekly_analysis_tool_data_to_dict("Ryan Data Dist Week by Week All Actives.zip"), 'active_profiles')

db.DatabaseWork().update_database_with_weekly_values(pull_weekly_analysis_tool_data_to_dict(
    "Ryan Data Dist Week by Week Total Profiles.zip"), 'overall_profiles')

"""
db.DatabaseWork().update_database_with_weekly_values(pull_weekly_analysis_tool_data_to_dict(
    "Ryan Data Dist Week by Week Combined Salary.zip", medians=True), 'combined_salary_weekly', medians=True)

db.DatabaseWork().update_database_with_weekly_values(pull_weekly_analysis_tool_data_to_dict(
    "Ryan Data Dist Week by Week EAC Medians.zip", medians=True), 'eac_weekly', medians=True)
"""

monthly_zip = [("Ryan Data Dist ONET 40.zip", 'onet_forty'),
               ("Ryan Data Dist ONET 40 Overall.zip", 'onet_forty_overall'),
               ("Ryan Data Dist Month by Month NAICS 40.zip", 'naics_codes'),
               ("Ryan Data Dist Month by Month NAICS 40 Overall.zip", 'naics_codes_overall'),
               ("Ryan Data Dist Metros.zip", 'metro_main'),
               ("Ryan Data Dist Metros Overall.zip", 'metro_main_overall'),
               ("Ryan Data Dist Degree Affinities.zip", 'degree_affinities'),
               ("Ryan Data Dist Degree Affinities Overall.zip", 'degree_affinities_overall'),
               ("Ryan Data Dist Company Sizes.zip", 'company_size'),
               ("Ryan Data Dist Company Sizes Overall.zip", 'company_size_overall'),
               ("Ryan Data Dist Age Buckets.zip", 'age_ranges'),
               ("Ryan Data Dist Age Buckets Overall.zip", 'age_ranges_overall'),
               ("Ryan Data Dist YE.zip", 'years_experience'),
               ("Ryan Data Dist YE Overall.zip", 'years_experience_overall'),
               ("Ryan Data Dist Rollups.zip", 'rollups'),
               ("Ryan Data Dist Rollups Overall.zip", 'rollups_overall')]

[db.DatabaseWork().update_database_with_monthly_values(pull_monthly_analysis_tool_data_to_dict(
    report_pair[0]), report_pair[1]) for report_pair in monthly_zip]
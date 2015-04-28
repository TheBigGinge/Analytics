import os
import zipfile

import AnalysisTool.deserialize_xml as xml_parse
import AnalysisTool.run_queries as execute
import DateFunctions.date_functions as dates
import data_dist_database as db
import run_analysis_queries as raq
import Statistics.chi_square as chi
import AnalysisTool.extract_data_xml as extract


class DataDistributions:

    def __init__(self):
        self.report_path = "\\\\psstats03\\reports\\"
        self.temp_in_files = "\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\temporary_files\\in_files\\"
        self.temp_out_files = "\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\temporary_files\\out_files\\"
        self.zip_path = "\\\\filer01\\public\\Data_Analytics\\Data Distributions\\temporary_files\\out_files\\"

        self.most_recent_sunday = dates.DateFunctions().find_most_recent_sunday()
        self.most_recent_sunday = dates.DateFunctions().datetime_to_string_y_m_d(self.most_recent_sunday, "-")
        self.first_of_month = dates.DateFunctions().return_ymd_first_of_the_current_month("-")

        self.monthly_zip = [("Ryan Data Dist ONET 40.zip", 'onet_forty'),
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

    def pull_count_data(self, file_name):

        return extract.ExtractXMLData(self.temp_out_files + file_name).overall_data_count()

    def pull_monthly_count_data(self, file_name):

        return extract.ExtractXMLData(self.temp_out_files + file_name).row_name_entry_handler()

    def pull_medians_data(self, file_name):

        return extract.ExtractXMLData(self.temp_out_files + file_name).overall_medians_list_return()

    def post_analysis_tool_query(self,
                                 index_server,
                                 in_file,
                                 start_date,
                                 end_date,
                                 main_filter,
                                 report_measure,
                                 return_type,
                                 first_dimension_file,
                                 second_dimension_file,
                                 dimension=None,
                                 ranges="Fixed"):

        execute.AnonReports(self.temp_in_files, self.temp_out_files).\
            post_analysis_tool_query_pre_made_file_dims(index_server,
                                                        in_file,
                                                        start_date,
                                                        end_date,
                                                        main_filter,
                                                        report_measure,
                                                        return_type,
                                                        first_dimension_file,
                                                        second_dimension_file,
                                                        dimension=dimension,
                                                        ranges=ranges)

    def zip_file_open(self, zip_file):

        full_zip_file = zipfile.ZipFile(self.temp_out_files + zip_file)
        file_list = full_zip_file.namelist()

        [full_zip_file.extract(file_name, self.temp_out_files) for file_name in file_list]

    def pull_weekly_analysis_tool_data_to_dict(self, zip_file, medians=False):

        self.zip_file_open(zip_file)

        file_name = zip_file[zip_file.rfind("\\") + 1:].strip(".zip")

        for files in os.listdir(self.temp_out_files):
            if file_name in files and "_" in files:

                xml_parse.fix_xml_encoding(self.zip_path, files)

                if medians is True:
                    print "Pulling data from " + files + "..."
                    weekly_dictionary = self.pull_medians_data(files)
                else:
                    print "Pulling data from " + files + "..."
                    weekly_dictionary = self.pull_count_data(files)

                return weekly_dictionary

    def pull_monthly_analysis_tool_data_to_dict(self, zip_file):
        self.zip_file_open(zip_file)

        file_name = zip_file[zip_file.rfind("\\") + 1:].strip(".zip")
        monthly_dictionary = {}

        for files in os.listdir(self.temp_out_files):
            if file_name in files and "_" in files:
                if "Overall" not in file_name and "Overall" in files:
                    continue
                else:
                    print "Pulling data from " + files + "..."

                    xml_parse.fix_xml_encoding(self.zip_path, files)

                    temporary_dictionary = self.pull_monthly_count_data(files)
                    monthly_dictionary.update(temporary_dictionary)

        return monthly_dictionary

    def update_weekly_database(self):

        db.DatabaseWork().update_database_with_weekly_values(
            self.pull_weekly_analysis_tool_data_to_dict("Ryan Data Dist Week by Week All Actives.zip"),
            'active_profiles')

        db.DatabaseWork().update_database_with_weekly_values(self.pull_weekly_analysis_tool_data_to_dict(
            "Ryan Data Dist Week by Week Total Profiles.zip"), 'overall_profiles')

    def update_monthly_database(self):

        [db.DatabaseWork().update_database_with_monthly_values(self.pull_monthly_analysis_tool_data_to_dict(
            report_pair[0]), report_pair[1]) for report_pair in self.monthly_zip]

    @staticmethod
    def run_weekly_analysis_tool_queries():
        raq.run_weekly_queries()

    @staticmethod
    def run_monthly_analysis_tool_queries():
        raq.run_monthly_queries()

    def create_weekly_statistics(self, active_list, total_list):

        current_distribution = []
        past_distribution = dict()
        past_distribution['active'] = 0
        past_distribution['total'] = 0
        last_sunday, six_weeks_prior = self.find_weekly_date_values()
        two_sundays_ago = str(dates.DateFunctions().find_date_two_sundays_ago().strftime("%Y%m%d"))

        for i in xrange(0, len(active_list) - 1):
            if str(active_list[i][0]) == two_sundays_ago:
                current_distribution.append(active_list[i][1])
                current_distribution.append(total_list[i][1] - active_list[i][1])
            else:
                past_distribution["active"] += active_list[i][1]
                past_distribution['total'] += total_list[i][1]

        current_distribution.append(past_distribution['active'])
        current_distribution.append(past_distribution['total'] - past_distribution['active'])

        current_ratio = float(current_distribution[0]) / float(current_distribution[1])
        past_ratio = float(past_distribution['active']) / float(past_distribution['total'])

        stats = chi.ChiSquaredIndependence(current_distribution)
        stats.calculate_expected_values()
        final_stats = stats.calculate_chi_square()

        return last_sunday, current_distribution[0], current_distribution[1], current_ratio, current_distribution[2], \
            current_distribution[3], past_ratio, final_stats[0], final_stats[1], current_ratio - past_ratio

    def create_monthly_statistics(self, active_list, total_list, category):

        past_actives = {}
        past_totals = {}

        last_month = dates.DateFunctions().return_ymd_first_of_last_month("")[:6]

        current_actives = {}
        current_total = {}

        [self.create_monthly_values_dictionary(item, past_actives) for item in active_list
         if last_month not in str(item[0])]
        [self.create_monthly_values_dictionary(item, past_totals) for item in total_list
         if last_month not in str(item[0])]
        [self.create_monthly_values_dictionary(key_trio, current_actives) for key_trio in active_list
         if last_month in str(key_trio[0])]
        [self.create_monthly_values_dictionary(key_trio, current_total) for key_trio in total_list
         if last_month in str(key_trio[0])]

        for keys in past_totals.keys():

            distribution_list = list()

            try:
                current_active_count = current_actives[keys]
            except KeyError:
                current_active_count = 0

            try:
                current_total_count = current_total[keys] - current_active_count
            except KeyError:
                current_total_count = 0

            distribution_list.append(current_active_count)
            distribution_list.append(current_total_count)

            try:
                current_ratio = float(current_active_count) / float(current_active_count + current_total_count)
            except ZeroDivisionError:
                current_ratio = 0

            try:
                past_active_count = past_actives[keys]
            except KeyError:
                past_active_count = 0

            distribution_list.append(past_active_count)
            distribution_list.append(past_totals[keys] - past_active_count)

            past_ratio = float(past_active_count) / float(past_totals[keys])

            pass_fail = True

            for number in distribution_list:
                if number in distribution_list <= 5:
                    pass_fail = False

            if pass_fail is True:
                stats = chi.ChiSquaredIndependence(distribution_list)
                stats.calculate_expected_values()
                final_stats = stats.calculate_chi_square()
            else:
                final_stats = ("N/A", "N/A")

            yield category, keys, current_active_count, current_total_count + current_active_count, current_ratio, \
                past_active_count, past_totals[keys], past_ratio, \
                final_stats[0], final_stats[1], current_ratio - past_ratio

    @staticmethod
    def create_monthly_values_dictionary(trio, target_dict):

        if trio[1] not in target_dict.keys():
            target_dict[trio[1]] = trio[2]
        else:
            target_dict[trio[1]] += trio[2]

    @staticmethod
    def find_monthly_date_values():
        first_of_month = dates.DateFunctions().return_ymd_first_of_the_current_month("")

        current_month = int(first_of_month[4:6])
        current_year = int(first_of_month[:4])

        for i in xrange(0, 6):
            current_month -= 1

            if current_month == 0:
                current_month += 12
                current_year -= 1

        current_month = str(current_month)
        if len(current_month) == 1:
            current_month = "0" + current_month

        return str(current_year) + current_month + "01", first_of_month

    @staticmethod
    def find_weekly_date_values():

        closest_sunday = dates.DateFunctions().find_most_recent_sunday()
        weeks_prior = dates.DateFunctions().create_prior_date_by_weeks(closest_sunday, 6)

        closest_sunday = str(closest_sunday.strftime("%Y%m%d"))
        weeks_prior = str(weeks_prior.strftime("%Y%m%d"))

        return closest_sunday, weeks_prior
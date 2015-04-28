import os
import sqlite3

import DateFunctions.date_functions as daten


class DatabaseWork:

    def __init__(self):
        self.file_path = "\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\"
        self.sql_data_base = "\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\" \
                             "Database\\distributions.db"

        self.table_lookup = {'naics_codes': 'code', 'naics_codes_overall': 'code',
                             'company_size': 'size_range', 'company_size_overall': 'size_range',
                             'age_ranges': 'age_range', 'age_ranges_overall': 'age_range',
                             'degree_affinities': 'level', 'degree_affinities_overall': 'level',
                             'years_experience': 'experience_range', 'years_experience_overall': 'experience_range',
                             'metro_main': 'key', 'metro_main_overall': 'key',
                             'onet_forty': 'code', 'onet_forty_overall': 'code',
                             'rollups': 'name', 'rollups_overall': 'name'}

    def __create_database(self):
        """
        Creating tables to store data from the Analysis Tool in. If there is a database already in place then
        all data will be wiped!!!
        """

        if os.path.isfile(self.sql_data_base) is True:
            os.remove(self.sql_data_base)

        conn = sqlite3.connect(self.sql_data_base)

        print("Creating tables in the sql data base... \n")
        c = conn.cursor()

        c.execute('''CREATE TABLE active_profiles (date INTEGER, profiles INTEGER)''')

        c.execute('''CREATE TABLE overall_profiles (date INTEGER, profiles INTEGER)''')

        c.execute('''CREATE TABLE eac_weekly (date INTEGER, twenty_fifth INTEGER, median INTEGER,
                  seventy_fifth INTEGER)''')

        c.execute('''CREATE TABLE combined_salary_weekly (date INTEGER, twenty_fifth INTEGER, median INTEGER,
                  seventy_fifth INTEGER)''')

        c.execute('''CREATE TABLE naics_codes (date INTEGER, code INTEGER, profiles INTEGER)''')

        c.execute('''CREATE TABLE naics_names (code INTEGER PRIMARY KEY NOT NULL, name text)''')

        c.execute('''CREATE TABLE naics_codes_overall (date INTEGER, code INTEGER, profiles INTEGER)''')

        c.execute('''CREATE TABLE company_size (date INTEGER, size_range TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE company_size_overall (date INTEGER, size_range TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE age_ranges (date INTEGER, age_range TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE age_ranges_overall (date INTEGER, age_range TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE degree_affinities (date INTEGER, level TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE degree_affinities_overall (date INTEGER, level TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE years_experience (date INTEGER, experience_range TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE years_experience_overall ( date INTEGER, experience_range TEXT,
                  profiles INTEGER)''')

        c.execute('''CREATE TABLE metro_key (key INTEGER, country TEXT, state TEXT, city TEXT)''')

        c.execute('''CREATE TABLE metro_name (key INTEGER PRIMARY KEY NOT NULL, name TEXT)''')

        c.execute(''' CREATE TABLE metro_main (date INTEGER, key INTEGER, profiles INTEGER)''')

        c.execute(''' CREATE TABLE metro_main_overall (date INTEGER, key INTEGER, profiles INTEGER)''')

        c.execute('''CREATE TABLE onet_name (code TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE onet_forty (date INTEGER, code TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE onet_forty_overall (date INTEGER, code TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE rollups (date INTEGER, name TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE rollups_overall (date INTEGER, name TEXT, profiles INTEGER)''')

        c.execute('''CREATE TABLE rollups_key (job TEXT, rollup TEXT, onet40 TEXT)''')

        c.execute('''CREATE TABLE metro_rollups (date INTEGER, rollup TEXT, metro_key INTEGER, profiles INTEGER)''')

        c.execute('''CREATE TABLE metro_rollups_overall (date INTEGER, rollup TEXT, metro_key INTEGER,
        profiles INTEGER)''')

        conn.commit()
        conn.close()

    def update_database_with_weekly_values(self, count_dict, data_table, medians=False):
        #Inserting data into the created tables
        if medians is False:
            print('Placing data into ' + data_table + ' \n')
            conn = sqlite3.connect(self.sql_data_base)
            c = conn.cursor()

            for keys in count_dict:
                use_date = daten.DateFunctions().return_full_year_month_day(str(keys))
                c.execute('INSERT INTO ' + data_table + ' VALUES (?,?)',
                          (use_date, count_dict[keys]))

            conn.commit()
            conn.close()

        elif medians is True:
            print('Placing data into ' + data_table + ' \n')
            conn = sqlite3.connect(self.sql_data_base)
            c = conn.cursor()

            for keys in count_dict:
                use_date = daten.DateFunctions().return_full_year_month_day(str(keys))

                twenty_fifth = count_dict[keys][1]
                median = count_dict[keys][2]
                seventy_fifth = count_dict[keys][3]

                c.execute('INSERT INTO eac_weekly VALUES (?,?,?,?)', (use_date, twenty_fifth, median, seventy_fifth))

            conn.commit()
            conn.close()

    def update_database_with_monthly_values(self, dictionary, data_table,  mapping=None, rollup_metro=False):

        conn = sqlite3.connect(self.sql_data_base)
        c = conn.cursor()

        if rollup_metro is False:
            print('Placing data into ' + data_table + ' \n')
            for keys in dictionary:
                use_date = daten.DateFunctions().return_full_year_month_day(str(keys))
                category = set()
                [category.add(new_key) for new_key in dictionary[keys] if new_key is not None]
                for i, value in enumerate(category):
                    profiles = dictionary[keys][value]

                    if mapping is None:
                        c.execute('INSERT INTO ' + data_table + ' VALUES (?,?,?)', (use_date, value, profiles))
                    if mapping is not None:
                        c.execute('INSERT INTO ' + data_table + ' VALUES (?,?,?)', (use_date, mapping[value],
                                                                                    profiles))

        elif rollup_metro is True:
            for keys in dictionary:
                use_date = daten.DateFunctions().return_full_year_month_day(keys)
                category = set()
                [category.add(new_key) for new_key in dictionary[keys] if new_key is not None]
                for i, value in enumerate(category):
                    data_list = dictionary[keys][value]
                    for pair in data_list:
                        rollup = pair[0]
                        profiles = pair[1]

                        c.execute('INSERT INTO ' + data_table + ' VALUES (?,?,?,?)', (use_date, rollup, mapping[value],
                                                                                      profiles))
        conn.commit()
        conn.close()

    def pull_monthly_values(self, table, start, end, employer_size=False):

        out_put = []
        conn = sqlite3.connect(self.sql_data_base)
        c = conn.cursor()

        query = "SELECT date, " + self.table_lookup[table] + ", profiles FROM " + table + " WHERE " +\
                "date <= " + start + " and date >= " + end

        if employer_size is False:
            for row in c.execute(str(query)):
                results = row[0], row[1], row[2]
                out_put.append(results)
        else:
            for row in c.execute(str(query)):
                results = row[0], row[1] + " Employees", row[2]
                out_put.append(results)

        conn.close()

        return out_put

    def pull_weekly_values(self, table, start, end):

        out_put = []
        conn = sqlite3.connect(self.sql_data_base)
        c = conn.cursor()

        query = "SELECT date, profiles FROM " + table + " WHERE " +\
                "date <= " + start + " and date >= " + end

        for row in c.execute(str(query)):
            results = row[0], row[1]
            out_put.append(results)

        conn.close()

        return out_put

    def pull_most_recent_date_value(self, table):

        dates = []

        conn = sqlite3.connect(self.sql_data_base)
        c = conn.cursor()

        query = "SELECT date FROM " + table

        for items in c.execute(str(query)):
            dates.append(int(items[0]))

        conn.close()

        return max(dates)
import sqlite3
import os

data_path = '\\\\filer01\\public\\Data_Analytics\\Consumer Log Metrics\\Data Files\\'
log_path_write = '\\\\filer01\\public\\Data_Analytics\\Consumer_Level_Conversion\\'
log_path = '\\\\psfiler01\\data\\SurveyReports\\'


class CreateDataBase:

    def __init__(self):
        self.__create_database()

    @staticmethod
    def __create_database():

        """
        WARNING! This is for completely starting over only. THIS ERASES ALL OF THE CURRENT DATABASE
        and then creates a new one from scratch. Only use when you're fixing bugs with counting log data
        and need to start over.

        Update:
            Level_90 was added after the fact which is why the ordering is weird. If you have time
            and feel it to be necessary rearrange the database to have level_90 before SawMyPayScale
            and then rebuild the entire database plus alter the way the optional level counting is handled.
        """
        if os.path.isfile(log_path_write + "Data\\Conversions.db") is True:
            os.remove(log_path_write + "Data\\Conversions.db")

        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")

        print("Creating tables in the sql data base... \n")
        c = conn.cursor()

        '''Creating tables to store data from the Log Files in'''
        c.execute('''CREATE TABLE FastTrack (date INTEGER, level_15 INTEGER, level_20 INTEGER, level_30 INTEGER,
         level_50 INTEGER, level_60 INTEGER, level_70 INTEGER, level_80 INTEGER,
         level_90 INTEGER, SawMyPayScale INTEGER)''')

        c.execute('''CREATE TABLE FastTrack_Edit (date INTEGER, level_15 INTEGER, level_20 INTEGER, level_30 INTEGER,
         level_50 INTEGER, level_60 INTEGER, level_70 INTEGER, level_80 INTEGER,
         level_90 INTEGER, SawMyPayScale INTEGER)''')

        c.execute('''CREATE TABLE JobOffer (date INTEGER, level_15 INTEGER, level_20 INTEGER, level_30 INTEGER,
         level_50 INTEGER, level_60 INTEGER, level_70 INTEGER, level_80 INTEGER,
         level_90 INTEGER, SawMyPayScale INTEGER)''')

        c.execute('''CREATE TABLE level_20 (date INTEGER, survey TEXT, level_20 INTEGER, level_30 INTEGER,
         level_50 INTEGER,  level_60 INTEGER, level_70 INTEGER, level_80 INTEGER,
         level_90 INTEGER, SawMyPayScale INTEGER)''')

        c.execute('''CREATE TABLE level_60 (date INTEGER, survey TEXT,
         level_60 INTEGER, level_70 INTEGER, level_80 INTEGER,
         level_90 INTEGER, SawMyPayScale INTEGER)''')

        c.execute('''CREATE TABLE level_80 (date INTEGER, survey TEXT,
         level_80 INTEGER, level_90 INTEGER,
         SawMyPayScale INTEGER)''')

        c.execute('''CREATE TABLE level_90 (date INTEGER, survey TEXT,
         level_90 INTEGER,
         SawMyPayScale INTEGER)''')

        #c.execute('''CREATE TABLE level_80 (date INTEGER, survey TEXT,
        # level_80 INTEGER, level_90 INTEGER,
        # SawMyPayScale INTEGER)''')

        #c.execute('''CREATE TABLE level_90 (date INTEGER, survey TEXT, level_90 INTEGER, SawMyPayScale INTEGER''')

        conn.commit()
        conn.close()


class DataBaseQueries:

    def __init__(self):
        self.fancy = None

    @staticmethod
    def pull_overall_data(min_date, max_date, survey_type):

        #Pull all of the relevant conversion levels from the database and place in a dictionary

        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        conversion_dict = {}

        query = "SELECT level_15, level_20, level_30, level_50, level_60, level_70, level_80, level_90, " \
                "SawMyPayScale FROM " + survey_type + " WHERE date >= " + min_date + " AND date <= " + max_date

        level_15 = 0
        level_20 = 0
        level_30 = 0
        level_50 = 0
        level_60 = 0
        level_70 = 0
        level_80 = 0
        level_90 = 0
        saw_my_payscale = 0

        level_list_names = ["level_15", "level_20", "level_30", "level_50", "level_60",
                            "level_70", "level_80", "level_90", "SawMyPayScale"]

        for row in c.execute(query):
            level_15 += row[0]
            level_20 += row[1]
            level_30 += row[2]
            level_50 += row[3]
            level_60 += row[4]
            level_70 += row[5]
            level_80 += row[6]
            level_90 += row[7]

            saw_my_payscale += row[8]

        level_list = [level_15, level_20, level_30, level_50, level_60,
                      level_70, level_80, level_90, saw_my_payscale]

        #only return counts for levels that are higher than other levels
        #level_20 over level_15 instead of level_15 over level_20
        #No ratios > 1 are returned unless there log file errors
        for i, levels in enumerate(level_list):
            for x, comparison_levels in enumerate(level_list):
                if level_list_names[i] == level_list_names[x]:
                    continue
                elif x < i:
                    continue
                elif "20" in level_list_names[i] or "60" in level_list_names[i] or "80" in level_list_names[i] \
                        or "90" in level_list_names[i]:
                    continue
                else:
                    dict_key = "Converted to " + level_list_names[x] + " from " + level_list_names[i]
                    values = level_list[x], level_list[i]
                    conversion_dict[dict_key] = values

        conn.close()
        return conversion_dict

    @staticmethod
    def pull_max_date():

        #used to determine the last day the sql_lite database was updated
        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        query = "SELECT date FROM FastTrack"
        query_two = "SELECT date FROM JobOffer"

        all_dates = []

        for row in c.execute(query):
            date = row[0]
            all_dates.append(date)

        for row in c.execute(query_two):
            date = row[0]
            all_dates.append(date)

        conn.close()

        return max(all_dates)

    @staticmethod
    def pull_all_used_dates():

        #used to find all dates used in the database so far so you can find the log files
        #that still need to be counted
        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        query = "SELECT * FROM level_20"

        all_dates = set()

        for row in c.execute(query):
            date = str(row[0])
            all_dates.add(date)

        conn.close()

        return all_dates

    @staticmethod
    def check_for_date_existence(test_date):

        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        date_exists = True

        query = "Select level_70 FROM FastTrack where date = " + test_date

        try:
            for row in c.execute(query):
                check = row[0]
        except:
            date_exists = False
            conn.close()

        return date_exists

    @staticmethod
    def pull_conversions_for_optional_levels(level_name, survey_type, min_date, max_date):

        name_dictionary = {"level_20": ["level_20", "level_30",
                                        "level_50", "level_60", "level_70", "level_80",
                                        "level_90", "SawMyPayScale"],
                           "level_60": ["level_60", "level_70", "level_80", "level_90", "SawMyPayScale"],
                           "level_80": ["level_80", "level_90", "SawMyPayScale"],
                           "level_90": ["level_90", "SawMyPayScale"]}

        conversion_dict = {}

        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        query = "SELECT *" \
                " FROM " + level_name + " WHERE date >= " + min_date + " AND date <= " + max_date + " AND survey = '"\
                + survey_type + "'"

        level_list_names = name_dictionary[level_name]

        level_list = DataBaseQueries.count_values_from_database(c, query, level_name)

        for i, levels in enumerate(level_list):
            if i == 0:
                continue
            else:
                ratio = level_list[i], level_list[0]
                key = "Converted to " + level_list_names[i] + " from " + level_list_names[0]
                conversion_dict[key] = ratio

        conn.close()

        return conversion_dict

    @staticmethod
    def count_values_from_database(connection, query, level_name):

        if level_name == "level_20":
            level_20 = 0
            level_30 = 0
            level_50 = 0
            level_60 = 0
            level_70 = 0
            level_80 = 0
            level_90 = 0
            saw_my_payscale = 0

            for row in connection.execute(query):
                level_20 += row[2]
                level_30 += row[3]
                level_50 += row[4]
                level_60 += row[5]
                level_70 += row[6]
                level_80 += row[7]
                level_90 += row[8]
                saw_my_payscale += row[9]

            level_list = [level_20, level_30, level_50, level_60,
                          level_70, level_80, level_90, saw_my_payscale]

        elif level_name == "level_60":
            level_60 = 0
            level_70 = 0
            level_80 = 0
            level_90 = 0
            saw_my_payscale = 0

            for row in connection.execute(query):
                level_60 += row[2]
                level_70 += row[3]
                level_80 += row[4]
                level_90 += row[5]
                saw_my_payscale += row[6]

            level_list = [level_60, level_70, level_80, level_90, saw_my_payscale]

        elif level_name == "level_80":
            level_80 = 0
            level_90 = 0
            saw_my_payscale = 0

            for row in connection.execute(query):
                level_80 += row[2]
                level_90 += row[3]
                saw_my_payscale += row[4]

            level_list = [level_80, level_90, saw_my_payscale]

        else:
            level_90 = 0
            saw_my_payscale = 0

            for row in connection.execute(query):
                level_90 += row[2]
                saw_my_payscale += row[3]

            level_list = [level_90, saw_my_payscale]

        return level_list

    @staticmethod
    def delete(table):
        """
        Delete the Data!
        """

        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        query = "DELETE FROM " + table + " WHERE date <= 20140512 and date >= 20130708;"

        c.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def find_the_dates():

        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        query = "SELECT date FROM FastTrack WHERE level_40 = 0"

        for row in c.execute(query):
            print row

        conn.close()

    def data_to_database(self, temp_count_dict, use_date):

        #self.text_edit.append("Placing data in database...")
        print "Placing data in database..."
        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        all_keys = temp_count_dict.keys()
        for keys in all_keys:

            key_name = keys.replace("-", "_")
            level_15 = self.key_try(temp_count_dict, keys, "level_15")
            level_20 = self.key_try(temp_count_dict, keys, "level_20")
            level_30 = self.key_try(temp_count_dict, keys, "level_30")
            level_50 = self.key_try(temp_count_dict, keys, "level_50")
            level_60 = self.key_try(temp_count_dict, keys, "level_60")
            level_70 = self.key_try(temp_count_dict, keys, "level_70")
            level_80 = self.key_try(temp_count_dict, keys, "level_80")
            level_90 = self.key_try(temp_count_dict, keys, "level_90")
            saw_my_payscale = self.key_try(temp_count_dict, keys, "SawMyPayScale")

            c.execute('INSERT INTO ' + key_name + ' VALUES (?,?,?,?,?,?,?,?,?,?)', (use_date, level_15, level_20,
                                                                                    level_30, level_50,
                                                                                    level_60, level_70, level_80,
                                                                                    level_90, saw_my_payscale))

        conn.commit()
        conn.close()

    def data_to_level_tables_in_database(self, temp_level_count_dict, use_date):

        #self.text_edit.append("Placing data in database...")
        print "Placing optional data in database..."
        conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
        c = conn.cursor()

        all_keys = temp_level_count_dict.keys()

        for keys in all_keys:

            for second_keys in temp_level_count_dict[keys]:

                if "20" in keys:
                    key_name = keys.replace("-", "_")
                    level_20 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_20")
                    level_30 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_30")
                    level_50 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_50")
                    level_60 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_60")
                    level_70 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_70")
                    level_80 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_80")
                    level_90 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_90")
                    saw_my_payscale = self.level_key_try(temp_level_count_dict, keys, second_keys, "SawMyPayScale")

                    c.execute('INSERT INTO ' + key_name + ' VALUES (?,?,?,?,?,?,?,?,?,?)', (use_date, second_keys,
                                                                                            level_20, level_30,
                                                                                            level_50,
                                                                                            level_60, level_70,
                                                                                            level_80,
                                                                                            level_90, saw_my_payscale))
                #Level 90 was created after the fact so it needs to be inserted last
                elif "60" in keys:
                    key_name = keys.replace("-", "_")
                    level_60 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_60")
                    level_70 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_70")
                    level_80 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_80")
                    level_90 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_90")
                    saw_my_payscale = self.level_key_try(temp_level_count_dict, keys, second_keys, "SawMyPayScale")

                    c.execute('INSERT INTO ' + key_name + ' VALUES (?,?,?,?,?,?,?)', (use_date, second_keys,
                                                                                      level_60, level_70,
                                                                                      level_80,
                                                                                      level_90, saw_my_payscale))

                #Level 90 was created after the fact so it needs to be inserted last
                elif "80" in keys:
                    key_name = keys.replace("-", "_")
                    level_80 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_80")
                    level_90 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_90")
                    saw_my_payscale = self.level_key_try(temp_level_count_dict, keys, second_keys, "SawMyPayScale")

                    c.execute('INSERT INTO ' + key_name + ' VALUES (?,?,?,?,?)', (use_date, second_keys,
                                                                                  level_80,
                                                                                  level_90, saw_my_payscale))

                elif "90" in keys:
                    key_name = keys.replace("-", "_")
                    level_90 = self.level_key_try(temp_level_count_dict, keys, second_keys, "level_90")
                    saw_my_payscale = self.level_key_try(temp_level_count_dict, keys, second_keys, "SawMyPayScale")

                    c.execute('INSERT INTO ' + key_name + ' VALUES (?,?,?,?)', (use_date, second_keys,
                                                                                level_90, saw_my_payscale))

        conn.commit()
        conn.close()

    @staticmethod
    def level_key_try(temp_level_count_dict, keys, second_keys, specified_level):
        try:
            final = temp_level_count_dict[keys][second_keys][specified_level]
        except KeyError:
            final = 0

        return final

    @staticmethod
    def key_try(temp_count_dict, keys, level):

        try:
            final = temp_count_dict[keys][level]
        except KeyError:
            final = 0

        return final

import sqlite3
import os

import FileHandling.file_work as fw
import database_utilities as util


class CreateDataBase:

    database_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\Database\\"
    main_file_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\"

    def __init__(self):
        self.__wipe_database_clean()
        self.__create_database()
        self.__create_breadth_thirty_databases()
        self.__create_breadth_forty_databases()
        self.__create_breadth_fifty_databases()
        self.__create_breadth_sixty_databases()

    def __wipe_database_clean(self):
        for db in ['Question_Database.db', 'breadth_thirty.db', 'breadth_forty.db', 'breadth_fifty.db,'
                                                                                    'breadth_sixty.db']:
            if os.path.exists(self.database_path + db):
                print "Removing old databases..."
                os.remove(self.database_path + db)

    def __create_database(self):

        conn = sqlite3.connect(self.database_path + "Question_Database.db")

        print("Creating tables in the main data base... \n")

        c = conn.cursor()
        '''Creating tables to store data from the Log Files in'''
        self.create_tables(c, util.get_all_the_questions())
        conn.close()

    @staticmethod
    def create_tables(c, question_list):

        for question in question_list:
            c.execute('''CREATE TABLE ''' + question.replace("/", "_").replace(" ", "_").replace("-", "_") +
                      ''' (date INTEGER, onet_code TEXT, numerator_count INTEGER,
                      bailed_20 INTEGER, saw_20 INTEGER, saw_my_payscale INTEGER,
                      total_shown INTEGER)''')

    def __create_breadth_thirty_databases(self):

        conn = sqlite3.connect(self.database_path + "breadth_thirty.db")

        print("Creating tables in the thirty data base... \n")

        c = conn.cursor()
        self.create_tables(c, util.get_all_the_questions())
        conn.close()

    def __create_breadth_forty_databases(self):

        conn = sqlite3.connect(self.database_path + "breadth_forty.db")

        print("Creating tables in the forty data base... \n")

        c = conn.cursor()
        self.create_tables(c, util.get_all_the_questions())
        conn.close()

    def __create_breadth_fifty_databases(self):

        conn = sqlite3.connect(self.database_path + "breadth_fifty.db")

        print("Creating tables in the fifty data base... \n")

        c = conn.cursor()
        self.create_tables(c, util.get_all_the_questions())
        conn.close()

    def __create_breadth_sixty_databases(self):

        conn = sqlite3.connect(self.database_path + "breadth_sixty.db")

        print("Creating tables in the sixty data base... \n")

        c = conn.cursor()
        self.create_tables(c, util.get_all_the_questions())
        conn.close()


class QuestionDashboardData:

    database_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\Database\\"
    main_file_path = "\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\"

    def __init__(self):
        self.fancy = 'fancy'

    def insert_numerator_dictionary_to_database(self, target_dictionary, start_date, header):
        conn = sqlite3.connect(self.database_path + "Question_Database.db")
        c = conn.cursor()

        data_date = self.change_string_date(str(start_date.date().toPyDate()))
        print "Inserting data in to the numerator dictionary..."
        for key_value in target_dictionary:

            question = header.replace("/", "_").replace(" ", "_").replace("-", "_")
            onet = key_value[key_value.find("/PayScale Code ") + len("/PayScale Code "):].strip()
            target_count = target_dictionary[key_value]

            c.execute('INSERT INTO ' + question + ' (date, onet_code, numerator_count) VALUES (?,?,?)',
                      (data_date, onet, target_count))

        conn.commit()
        conn.close()
        print "Completed."

    def insert_data_from_dict_to_database(self, denom_dict, num_dict, start_date):

        conn = sqlite3.connect(self.database_path + "Question_Database.db")
        c = conn.cursor()
        data_date = str(start_date)
        print "Inserting data into the database..."

        for question in denom_dict:
            for soc in denom_dict[question]:
                try:
                    num = num_dict[question.replace("/", "_").replace(" ", "_").replace("-", "_")][soc]
                except KeyError:
                    num = 0

                total = self.dictionary_pull(denom_dict, question, soc, 'total_shown')
                bailed_20 = self.dictionary_pull(denom_dict, question, soc, 'bailed_20')
                saw_20 = self.dictionary_pull(denom_dict, question, soc, 'saw_20')
                saw_payscale = self.dictionary_pull(denom_dict, question, soc, 'saw_payscale')
                c.execute('INSERT INTO ' + question.replace("/", "_").replace(" ", "_").replace("-", "_")
                          + ' VALUES(?,?,?,?,?,?,?)', (data_date, soc, num, bailed_20, saw_20, saw_payscale, total))

        conn.commit()
        conn.close()
        print "Completed."

    @staticmethod
    def dictionary_pull(dictionary, question, soc, value):
        try:
            final = dictionary[question][soc][value]
        except KeyError:
            final = 0
        return final

    def check_for_data(self):

        conn = sqlite3.connect(self.database_path + "Question_Denominator.db")
        c = conn.cursor()

        for i, question in enumerate(util.get_all_the_questions()):
            if 1 < 10:

                query = "SELECT date FROM " + question.replace("/", "_").replace(" ", "_").replace("-", "_")

                for row in c.execute(str(query)):
                    print row
            else:
                break

        conn.close()

    @staticmethod
    def change_string_date(string_date):
        year = string_date[:string_date.find("-")]
        new_string = string_date[string_date.find("-") + 1:]
        month = new_string[:new_string.rfind("-")]
        return year + month

    def get_all_dates(self):

        conn = sqlite3.connect(self.database_path + "Question_Database.db")
        c = conn.cursor()

        all_dates = []

        query = 'SELECT date FROM Certifications_Certifications'
        for row in c.execute(str(query)):
            all_dates.append(row[0])

        conn.close()

        return list(set(all_dates))

    def pull_all_non_breadth_data(self, question, date):

        assert isinstance(date, str), 'Date needs to be a string date of type %Y%m'

        conn = sqlite3.connect(self.database_path + "Question_Database.db")
        c = conn.cursor()

        query = 'SELECT * from ' + \
                question.replace("/", "_").replace(" ", "_").replace("-", "_") + ' WHERE date = ' + date

        for row in c.execute(str(query)):
            yield row

    def find_breadth_x_soc_codes(self, x):

        main_file = fw.FileHandler()

        if x == '30':
            breadth = 'All Breadth 30'
        elif x == '40':
            breadth = 'All Breadth 40'
        elif x == '50':
            breadth = 'All Breadth 50'
        else:
            breadth = 'All Breadth 60'

        soc_list = []

        for row in main_file.open_csv(self.main_file_path + "Onet_Breadths.csv"):
            soc = row[main_file.header.index(breadth)]
            soc_list.append(soc)

        return list(set(soc_list))

    def create_full_breadth_x_num_dictionary(self, x):

        count_dictionary = {}

        for question in util.get_all_the_questions():
            count_dictionary[question] = {}
            for soc in self.find_breadth_x_soc_codes(x):
                count_dictionary[question][soc] = 0

        return count_dictionary

    def data_to_breadth_x_db(self, start_date, x):

        if x == '30':
            breadth = 'thirty'
            digit = 7
            add = '.00'
        elif x == '40':
            breadth = 'forty'
            digit = 6
            add = '0.00'
        elif x == '50':
            breadth = 'fifty'
            digit = 5
            add = '00.00'
        else:
            breadth = 'sixty'
            digit = 4
            add = '000.00'

        count_dictionary = self.create_full_breadth_x_dictionary(x)

        for question in util.get_all_the_questions():
            for row in self.pull_all_non_breadth_data(question, start_date):

                soc = str(row[1])
                soc = soc[:digit] + add
                try:
                    count_dictionary[question][soc]['numerator_count'] = row[2]
                    count_dictionary[question][soc]['bailed_20'] = row[3]
                    count_dictionary[question][soc]['saw_20'] = row[4]
                    count_dictionary[question][soc]['saw_my_payscale'] = row[5]
                    count_dictionary[question][soc]['total_shown'] = row[6]
                except KeyError:
                    continue

        print "Inserting data into breadth " + breadth + " database..."

        conn = sqlite3.connect(self.database_path + "breadth_" + breadth + ".db")
        c = conn.cursor()

        for question in count_dictionary:
            for soc in count_dictionary[question]:
                answers = count_dictionary[question][soc]
                numerator = answers['numerator_count']
                bail = answers['bailed_20']
                saw = answers['saw_20']
                my_payscale = answers['saw_my_payscale']
                total = answers['total_shown']

                question_alt = question.replace("/", "_").replace(" ", "_").replace("-", "_")
                c.execute('INSERT INTO ' + question_alt + ' VALUES(?,?,?,?,?,?,?)',
                          (start_date, soc, numerator, bail, saw, my_payscale, total))

        conn.commit()
        conn.close()

    def create_full_breadth_x_dictionary(self, x):

        count_dictionary = {}

        for question in util.get_all_the_questions():
            count_dictionary[question] = {}
            for soc in self.find_breadth_x_soc_codes(x):
                count_dictionary[question][soc] = {}
                for answer in ['numerator_count', 'bailed_20', 'saw_20', 'saw_my_payscale', 'total_shown']:
                    count_dictionary[question][soc][answer] = 0

        return count_dictionary

    def pull_breadth_x_data(self, question, date, breadth):

        assert isinstance(date, str), 'Date needs to be a string date of type %Y%m'

        conn = sqlite3.connect(self.database_path + "breadth_" + breadth + ".db")
        c = conn.cursor()

        query = 'SELECT * from ' + \
                question.replace("/", "_").replace(" ", "_").replace("-", "_") + " WHERE date = " + date

        for row in c.execute(str(query)):
            yield row
import sqlite3
import liquid_support as ls


class LiquidData:

    def __init__(self):
        self.database_path = "C:\\LiquidPlanner\\"

    def create_database(self):

        conn = sqlite3.connect(self.database_path + "Liquid.db")

        print("Creating tables in the sql data base... \n")

        c = conn.cursor()
        '''Creating tables to store data from the Log Files in'''
        self.create_tables(c)

    @staticmethod
    def create_tables(c):

        c.execute('''CREATE TABLE tasks (task_id TEXT, name TEXT, updated_at TEXT, email_origin TEXT,
        earliest_start TEXT, expected_start TEXT, earliest_finish TEXT, expected_finish TEXT, is_done TEXT)''')

    def pull_all_current_tasks(self):
        all_task_ids = []
        all_task_dictionaries = []

        conn = sqlite3.connect(self.database_path + "Liquid.db")
        c = conn.cursor()

        query = 'SELECT task_id FROM tasks'
        all_query = 'SELECT * FROM tasks'

        for item in c.execute(str(query)):
            all_task_ids.append(item[0])

        for task_idents in all_task_ids:
            current_query = all_query + ' WHERE task_id = ' + task_idents
            all_tasks = {}
            for item in c.execute(str(current_query)):
                task_id, name, create_date, email_origin, earliest_start, expected_start, earliest_finish, \
                    expected_finish, is_done = item

                all_tasks['id'] = task_id
                all_tasks['name'] = name
                all_tasks['updated_at'] = create_date
                all_tasks['email_origin'] = email_origin
                all_tasks['earliest_start'] = earliest_start
                all_tasks['expected_start'] = expected_start
                all_tasks['earliest_finish'] = earliest_finish
                all_tasks['expected_finish'] = expected_finish
                all_tasks['is_done'] = is_done
                all_task_dictionaries.append(all_tasks)

        conn.close()

        return all_task_dictionaries

    def pull_all_task_items_to_dictionary(self, c, current_query):
        all_tasks = {}

        for item in c.execute(str(current_query)):
            task_id, name, create_date, email_origin, earliest_start, expected_start, earliest_finish, \
                expected_finish, is_done = item

            all_tasks['id'] = task_id
            all_tasks['name'] = name
            all_tasks['updated_at'] = create_date
            all_tasks['email_origin'] = email_origin
            all_tasks['earliest_start'] = earliest_start
            all_tasks['expected_start'] = expected_start
            all_tasks['earliest_finish'] = earliest_finish
            all_tasks['expected_finish'] = expected_finish
            all_tasks['is_done'] = is_done

    def insert_task_to_database(self, task_dict):

        task_id = task_dict['id']
        name = task_dict['name']
        create_date = task_dict['updated_at']
        email = ls.LiquidSupport().extract_email_from_note(str(task_id))
        earliest_start = task_dict['earliest_start']
        expected_start = task_dict['expected_start']
        earliest_finish = task_dict['earliest_finish']
        expected_finish = task_dict['expected_finish']
        is_done = str(task_dict['is_done'])

        if "Error" not in email:
            conn = sqlite3.connect(self.database_path + "Liquid.db")
            c = conn.cursor()

            c.execute('''INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?)''', (task_id, name, create_date, email,
                                                                           earliest_start, expected_start,
                                                                           earliest_finish,
                                                                           expected_finish, is_done))

            conn.commit()
            conn.close()

    def update_task_in_database(self, task_dict):
        task_id = task_dict['id']
        create_date = task_dict['updated_at']
        email = ls.LiquidSupport().extract_email_from_note(str(task_id))
        earliest_start = task_dict['earliest_start']
        expected_start = task_dict['expected_start']
        earliest_finish = task_dict['earliest_finish']
        expected_finish = task_dict['expected_finish']
        is_done = str(task_dict['is_done'])

        if "Error" not in email:
            conn = sqlite3.connect(self.database_path + "Liquid.db")
            c = conn.cursor()

            c.execute('''UPDATE tasks SET updated_at=?, earliest_start=?, expected_start=?, earliest_finish=?,
             expected_finish=?, is_done=? WHERE task_id=?''',
                      (create_date, earliest_start, expected_start, earliest_finish,
                      expected_finish, is_done, task_id))

            conn.commit()
            conn.close()
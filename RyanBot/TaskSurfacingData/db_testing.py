import sqlite3
import os


class TaskDataBase:

    def __init__(self):
        self.task_db = '\\\\filer01\\public\\Data_Analytics\\Task_Surfacing\\db\\TaskSurface.db'
        self.__create()

    def __create(self):
        if os.path.isfile(self.task_db) is True:
            os.remove(self.task_db)

        conn = sqlite3.connect(self.task_db)

        print("Creating tables in the sql data base... \n")
        c = conn.cursor()
        '''Creating tables to store data from the Log Files in'''

        c.execute('''CREATE TABLE task_surface (date INTEGER, guid TEXT, survey TEXT, job_title TEXT,
        chose_tasks INTEGER, do_not_apply INTEGER, visible INTEGER)''')

    def place_task_data(self, output_dict):
        conn = sqlite3.connect(self.task_db)
        c = conn.cursor()

        for guid_id in output_dict:
            final = output_dict[guid_id]
            entry_date = final[0], job_title = final[1], visible = final[2], do_not_apply = final[3], tasks = final[4],
            survey = final[5]

            c.execute('INSERT INTO task_surface VALUES (?,?,?,?)', (entry_date, guid_id, survey, job_title, tasks,
                                                                    do_not_apply, visible))




import liquid_sql_database as data
import liquid_support as ls
import RequestService.liquid_requests as lr
import sqlite3
import liquid_email as le

'''
lpr = lr.LiquidPlannerRequest()
workspace = lpr.workspaces()[0]
lpr.set_workspace_id(workspace['id'])
lpr.set_project_id(str(16976447))
'''


'''
database_path = "C:\\users\\ryanm\\Liquid_Planner\\"
conn = sqlite3.connect(database_path + "Questions.db")
c = conn.cursor()

query = "SELECT * from tasks"

c.execute(query)

conn.commit()
conn.close()


test = data.LiquidData()

for i, task in enumerate(test.pull_all_current_tasks()):
    if str(task['id']) == '17723422':
        le.LiquidEmail(task).send_new_task_message()

'''

#print test.pull_all_changes()

data.LiquidData().create_database()
#print data.LiquidData().pull_all_current_tasks()

#test = ls.LiquidSupport().current_active_tasks()
#for task in test:
#    if str(task['id']) == '17755520':
#        print task
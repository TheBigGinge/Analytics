from ScheduledDevTasks.LiquidPlanner import liquid_sql_database as lsd
from ScheduledDevTasks.LiquidPlanner import liquid_support as ls
from ScheduledDevTasks.LiquidPlanner import liquid_email as le
import os


#Create database if needed
if not os.path.isdir("C:\\LiquidPlanner\\"):
    os.makedirs("C:\\LiquidPlanner\\")
    lsd.LiquidData().create_database()

print "Finding current active tasks in liquid planner..."
lpr = ls.LiquidSupport()
current_active_tasks = lpr.current_active_tasks()
all_project_tasks = lpr.project_task_dictionaries

print "Finding currently stored tasks in our database..."
data = lsd.LiquidData()
stored_tasks = data.pull_all_current_tasks()
stored_task_ids = []

new_tasks = []

[stored_task_ids.append(str(value_id['id'])) for value_id in stored_tasks]

print "Inserting all new tasks into our database..."
[data.insert_task_to_database(task_dict) for task_dict in current_active_tasks
 if str(task_dict['id']) not in stored_task_ids]

[new_tasks.append(str(task_dict['id'])) for task_dict in current_active_tasks
 if str(task_dict['id']) not in stored_task_ids and "Error" not in
 lpr.extract_email_from_note(str(task_dict['id']))]

print "Checking tasks for changes..."
#Repull all tasks to pick up any new ones
all_stored_tasks = data.pull_all_current_tasks()

print "Checking for new tasks created..."
for task_dict in all_stored_tasks:

    if str(task_dict['id']) in new_tasks:
        print "Mailing newly created task..."
        le.LiquidEmail(task_dict).send_new_task_message()

for stored_task in all_stored_tasks:
    for liquid_task in all_project_tasks:
        if str(stored_task['id']) == str(liquid_task['id']):
            if lpr.check_for_task_changes(stored_task, liquid_task):
                print "Emailing changes..."
                data.update_task_in_database(liquid_task)

                le.LiquidEmail(stored_task, liquid_task).send_updated_message()

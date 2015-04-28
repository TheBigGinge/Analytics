import shutil
import sys
from db_testing import *
from FileHandling.file_work import *
from LogFileTools.log_iterator import *
from task_support import *

verbose_directory = '\\\\PSLT-078\\LogFiles\\VerboseLog\\'
log_directory = '\\\\filer01\\public\\Data_Analytics\\Task_Surfacing\\log_files\\'
sys.path.append("C:\\hg\\payscale\\users\\ryanm\\PayScaleAnalytics\\")


verbose_files = FileHandler()
verbose_files.find_all_files_inclusion(verbose_directory, 'ConsumerProfile_SelectedJobTasks')

for files in verbose_files.all_files_directory:
    shutil.move(verbose_directory + files, log_directory)

target_log_file = find_most_recently_created_file(log_directory)

db = TaskDataBase()

log_dict = {}
logger = CSVLogIterator(datetime.datetime(2014, 12, 1), datetime.datetime(2015, 1, 22))
logger.find_all_logs_survey()

for values in logger.iterate_files_return_row():

    survey = values[logger.header.index("SurveyType")]
    value = values[logger.header.index("ProfileGuid")]
    log_dict[value] = survey

task_logs = RawTaskLogSupport(log_dict)
task_logs.open_raw_task_file(target_log_file, log_directory)

db.place_task_data(task_logs.profile_dictionary)

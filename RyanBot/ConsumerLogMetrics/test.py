from LogFileTools import log_iterator
import datetime

csv_logs = log_iterator.CSVLogIterator(datetime.date(2013, 5, 1), datetime.date(2014, 5, 1))
csv_logs.find_all_logs_survey()

print csv_logs.log_files_to_use

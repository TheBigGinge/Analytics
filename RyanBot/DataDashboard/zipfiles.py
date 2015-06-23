import csv
import zipfile
import os

report_path = '\\\\filer01\\public\\Data Dashboards\\PSP Reports\\'
report_path_alt = '\\\\filer01\\public\\Data Dashboards\\PSP Zip Reports\\'
local_path = 'C:\\users\\ryanm\\desktop\\'

all_logs = os.listdir(report_path)

WorkingDir = os.getcwd()

log_files = "2015.06.csv"
'''
for log_files in all_logs:
    new_name = log_files.replace(".csv", ".zip")
    print new_name

    with zipfile.ZipFile(report_path_alt + new_name, 'w', zipfile.ZIP_DEFLATED) as create_zip:
        create_zip.write(report_path + log_files, arcname=log_files)

print "Complete"
'''

new_name = log_files.replace(".csv", ".zip")
print new_name


with zipfile.ZipFile(report_path_alt + new_name, 'w', zipfile.ZIP_DEFLATED) as create_zip:
    create_zip.write(report_path + log_files, arcname=log_files)

print "Complete"
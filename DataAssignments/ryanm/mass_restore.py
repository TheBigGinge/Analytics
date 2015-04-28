import zipfile
import os

stored_path = '\\\\filer01\\DBBACK\\analysistool\\'
analysis_path = '\\\\filer01\\DBBACK\\AnalysisToolReports\\'
pattern = 'KaylaTipping'

for files in os.listdir(stored_path):
    if pattern in files and ".zip" in files:
        full_zip_file = zipfile.ZipFile(stored_path + files)
        file_list = full_zip_file.namelist()

        [full_zip_file.extract(file_name, analysis_path) for file_name in file_list]
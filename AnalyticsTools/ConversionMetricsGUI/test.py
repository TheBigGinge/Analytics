import sqlite3
import os
import csv
import database

data_path = '\\\\pssea\\files\\public\\Data_Analytics\\Consumer Log Metrics\\Data Files\\'
log_path_write = '\\\\filer01\\public\\Data_Analytics\\Consumer_Level_Conversion\\'
log_path = '\\\\psfiler01\\data\\SurveyReports\\'

"""
if os.path.isfile(log_path_write + "Data\\Conversions.db") is True:
    print "Ok"

conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
c = conn.cursor()

c.execute('''CREATE TABLE level_90 (date INTEGER, survey TEXT,
 level_90 INTEGER,
 SawMyPayScale INTEGER)''')

conn.commit()
conn.close()
"""

"""
def log_line_pull(log_file_name):

    with open(log_path + log_file_name, 'rb') as R:
        reader = csv.reader(R, delimiter=',')
        global names
        names = reader.next()

        for row in reader:
            yield row


for i, row in enumerate(log_line_pull("surveyprofiledata-20140511.csv")):

    if i % 500 == 0 and i != 0:
        print "Processed %s lines..." % i
"""

"""
conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
c = conn.cursor()

c.execute('''ALTER TABLE FastTrack ADD COLUMN level_90 INTEGER DEFAULT 0''')
c.execute('''ALTER TABLE FastTrack_Edit ADD COLUMN level_90 INTEGER DEFAULT 0''')
c.execute('''ALTER TABLE JobOffer ADD COLUMN level_90 INTEGER DEFAULT 0''')
c.execute('''ALTER TABLE level_20 ADD COLUMN level_90 INTEGER DEFAULT 0''')
c.execute('''ALTER TABLE level_60 ADD COLUMN level_90 INTEGER DEFAULT 0''')
c.execute('''ALTER TABLE level_80 ADD COLUMN level_90 INTEGER DEFAULT 0''')

conn.commit()
conn.close()
"""

database.CreateDataBase()
# conn = sqlite3.connect(log_path_write + "Data\\Conversions.db")
# c = conn.cursor()


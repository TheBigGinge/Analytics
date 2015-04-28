import xlrd
import os

dash_path = '\\\\filer01\\public\\Data Dashboards\\Taxonomy Dashboards\\'


class DashReader:

    dash_boards = os.listdir(dash_path)

    def __init__(self):
        self.job_set = set()
        self.dash_board = ""
        self.recent_dashboard()
        self.pull_dash_data()
    
    def pull_dash_data(self):
        data_dashboard = self.dash_board
        print "Pulling in the Confirmed Jobs from " + data_dashboard + " \n"
        workbook = xlrd.open_workbook(filename=dash_path + data_dashboard)
        for sheet in workbook.sheets():
            if sheet.name != 'CFM':
                continue
            else:
                confirmed_jobs = map(str.strip, map(str, sheet.col_values(0)))
                for jobs in confirmed_jobs:
                    self.job_set.add(jobs)
        
    def recent_dashboard(self):
        #Find the mtimes for all the dashboards and then find the max
        #to get the most recent data dash board.
        file_dict = {}
        for files in DashReader.dash_boards:
            mtime = os.stat(dash_path + files).st_mtime
            file_dict[files] = mtime
        values = file_dict.values()
        current_time = max(values)
        for keys in file_dict:
            if file_dict[keys] == current_time:
                self.dash_board += keys
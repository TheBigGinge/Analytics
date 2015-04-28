import os
import csv
import datetime
import time
import xlrd


#Paths
Log_Files_Path = '\\\\psfiler01\\data\\SurveyReports\\'
Bogus_Profile_Path = '\\\\filer01\\public\\BogusProfiles\\Processed Log Files\\'
Disabled_Path = '\\\\filer01\\public\\BogusProfiles\\Profiles Disabled\\'
Dashboard_Path = '\\\\filer01\\public\\Data Dashboards\\Taxonomy Dashboards\\'
Rollup_Path = '\\\\filer01\\public\\BogusProfiles\\Current Rollups\\'

#Time Stuff
now = str(datetime.datetime.now())
todaysdate = now[:7]
todaysdate = todaysdate.replace('-', '')
todaysdateAlt = now[:7]


def create_date_for_disable_list():
    
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    
    month = +- 2
    
    if month <= 0:
        month += 12
        year -= 1

    month = str(month)
    if len(month) == 1:
        month = "0" + month
    
    final = str(year) + "-" + month
    
    return final
    
Disable_Date = create_date_for_disable_list()

time_now = time.asctime()
time_now = time_now.replace(":", "")

#Files
Bogus_Profiles = Disable_Date + ' disable_list.csv'
Log_Files = os.listdir('\\\\psfiler01\\data\\SurveyReports')
HUGE_CSV = todaysdate + ' Rob Bogus Profile Log VID.csv'
Test_File = 'Finger Print Test.csv'

Dash_Boards = os.listdir(Dashboard_Path)


class PullDashboardInformation:
    
    def __init__(self):
        new_dashboard = self.newest_dashboard()
        if self.dashboard_check(new_dashboard) is True:
            pass
        if self.dashboard_check(new_dashboard) is False:
            self.confirmed_dict = self.pull_rollups(new_dashboard)
            self.write_rollups_to_file()

    @staticmethod
    def newest_dashboard():
        
        #Pulls the most recent Data Dashboard
        file_dict = {}
        
        for files in Dash_Boards:
            if 'All Confirmed JobJobs' in files:
                continue
            else:
                mtime = os.stat(Dashboard_Path + files).st_mtime
                file_dict[files] = mtime
        items = file_dict.values()
        newest_time = max(items)
        for keys in file_dict:
            if file_dict[keys] == newest_time:
                return keys   

    @staticmethod
    def dashboard_check(new_dashboard):
        
        #Checks to see if this program has already written out the current Rollups
        
        for files in Rollup_Path:
            
            if new_dashboard[:7] in files:
                print "We already have the jobs we're looking for. No need to pull in jobs from the Data Dashboard. \n"
                return True
                
            else:
                return False

    @staticmethod
    def pull_rollups(new_dashboard):
        
        #Pulls Rollups and AnswerValues from the CFM tab in the most recent Data Dashboard and remove duplicates
        
        print "Pulling in the most recent information from the Data Dashboards \n"
        
        work_book = xlrd.open_workbook(filename=Dashboard_Path + new_dashboard)
        
        for sheet in work_book.sheets():
            if sheet.name != 'CFM':
                continue
            rule_value = map(str.strip, map(str, sheet.col_values(0)))
            answer_value = map(str.strip, map(str, sheet.col_values(6)))
            dashboard_name = new_dashboard[0:7]
            print "Pulling in the Confirmed Jobs from " + dashboard_name + " \n"
            
        confirmed_dict = dict(zip(rule_value, answer_value))
        
        return confirmed_dict

    def write_rollups_to_file(self):

        #Write the Rollups to a file in the Public Share
        
        print "Writing Rollups. \n"
        with open(Rollup_Path + todaysdate + ' job-rollups.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            header = ['Title', 'Rollup']
            writer.writerow(header)
            for row in self.confirmed_dict:
                final = row, self.confirmed_dict[row]
                writer.writerow(final)

PullDashboardInformation()


def five_month_survey_log_time(months):

    #Create the last 5 month, year combos for log file reading
    
    all_year_months = []
    current_months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    todays_date_2 = now[:7]
    current_year, current_month = todays_date_2.split("-")
    
    for i in range(months):
        current_date = current_months[int(current_month)-i-2]
        if int(current_month)-i-2 < 0:
            current_years = int(current_year)-1
        else:
            current_years = int(current_year)
        value = str(current_years)+str(current_date)
        all_year_months.append(value)
        
    return all_year_months
    

'''Regular Method currently commented out for a fingerprint test'''    
#AllYearMonths = Five_Month_Survey_Log_Timeline(5)    

'''Testing Finger Printing'''
all_years_months = five_month_survey_log_time(5)


class PullInformationFromLogs:

    #This pulls data out of the log files from the referenced columns

    def __init__(self):
        self.date_check()
        self.create_sheet()
        self.disabled_list = self.disable_list()
        self.log_files_list = self.gather_logs()
        self.log_file_iterator()

    @staticmethod
    def gather_logs():
        
        #Gather appropriate Log Files to a list
        
        log_files_list = []
        
        for i in range(0, len(all_years_months)):
            
            for files in Log_Files:
                if "aggregate" in files: continue
                    
                elif ".csv" not in files: continue
                
                elif "old" in files: continue
                
                elif all_years_months[i] in files:
                    log_files_list.append(files)
                    
        return log_files_list

    @staticmethod
    def date_check():
        
        #Keeps the program from rerunning if we've already done this month's
        
        if HUGE_CSV not in os.listdir(Bogus_Profile_Path):
            print "Current Compiled Log File is not up to date. Pulling in the past 5 months of logs now... \n"
        else:
            print "Everything is up to date. Now Exiting. \n"
            raise SystemExit

    @staticmethod
    def disable_list():
        
        #Pull in the list of disabled profiles from last month
        
        disabled_list = []
        
        with open(Disabled_Path + Bogus_Profiles, 'r') as f:
            z = csv.reader(f, delimiter=',')
            for row in z:
                G = row[5]
                disabled_list.append(G)
                
        disabled_list = set(disabled_list)
        
        return disabled_list

    @staticmethod
    def disabled_profile_check(guid, disabled_list):
        
        #Check to see if this profile has already been disabled
        
        if guid in disabled_list:
            disabled_profile = "Disabled"
        if guid not in disabled_list:
            disabled_profile = ""

        return disabled_profile

    @staticmethod
    def create_sheet():
        
        #Creates the file for the month and writes in the header row
        
        header = ['Date Check', 'VisitorId', 'SurveyType', 'IP', 'SurveyStartTime', 'ProfileGuid', 'Platform',
                  'Activated', 'Profile job', 'Profile userid', 'CompletedSurvey', 'SawMyPayscale',
                  'Employer\Employer Name Unprompted', 'Job\Job Unprompted', 'Profile city', 'Profile country',
                  'Profile employer', 'hasEmail', 'Profile state', 'Disabled']

        with open(Bogus_Profile_Path + HUGE_CSV, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(header)        

    @staticmethod
    def append_to_sheet(total_list):

        #Append current months data file
        
        print "Appending current month to file \n"
        
        with open(Bogus_Profile_Path + HUGE_CSV, 'a') as f:
#        with open(BogusPath + Test_File,'a') as f:   
            writer = csv.writer(f, lineterminator='\n')
            
            for spot in total_list:
                writer.writerow(spot) 

    def row_index(self, iterable, files, row_iter, names):

        #Grab indexed values by column name from the logs

        survey_type = row_iter[names.index('SurveyType')]
        visitor_id = row_iter[names.index('VisitorId')]
        ip = row_iter[names.index('IP')]
        start_time = row_iter[names.index('SurveyStartTime')]
        guid = row_iter[names.index('ProfileGuid')]
        platform = row_iter[names.index('Platform')]
        activated = row_iter[names.index('Activated')]
        profile_job = row_iter[names.index('Profile job')]
        user_id = row_iter[names.index('Profile userid')]
        #Changing complete to SawMyPayScale because of Consumer Log header bug
        #Technically this is a better measure of whether they completed the survey
        #2014-06-02
        complete = row_iter[names.index('SawMyPayscale')]
        saw_my_payscale = row_iter[names.index('SawMyPayscale')]
        employer_unprompted = row_iter[names.index('Employer\Employer Name Unprompted')]
        unprompted = row_iter[names.index('Job\Job Unprompted')]
        city = row_iter[names.index('Profile city')]
        country = row_iter[names.index('Profile country')]
        employer = row_iter[names.index('Profile employer')]
        email = row_iter[names.index('Profile hasEmail')]
        state = row_iter[names.index('Profile state')]
        name = files[iterable][len('surveyprofiledata-'):26]
            
        disabled = self.disabled_profile_check(guid, self.disabled_list)

        output = name, visitor_id, survey_type, ip, start_time, guid, platform, activated, profile_job, user_id, \
            complete, saw_my_payscale, employer_unprompted, unprompted, city, country, \
            employer, email, state, disabled
                     
        return output

    def log_file_iterator(self):
        
        #Main File Iterator that uses other methods to pull out the information and compile it
        
        total_list = []
        
        for i in range(0, len(self.log_files_list)):
            
            with open(Log_Files_Path + self.log_files_list[i], 'rb') as f:
                log_files = csv.reader(f, delimiter=',')

                names = log_files.next()
            
                print "Working on " + self.log_files_list[i]
                
                if "Profile job" in names:
                
                    for row in log_files:
                        output = self.row_index(i, self.log_files_list, row, names)

                        total_list.append(output)
                        
                    if i + 1 > len(self.log_files_list) - 1:
                            
                        self.append_to_sheet(total_list)
                                
                        total_list = []
                        
                    elif self.log_files_list[i][18:24] != self.log_files_list[i + 1][18:24]:
                        
                        self.append_to_sheet(total_list)
                                
                        total_list = []
                            

PullInformationFromLogs()

print "Program Complete"
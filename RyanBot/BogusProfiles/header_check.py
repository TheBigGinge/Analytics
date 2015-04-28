import csv
import datetime
import os

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

Log_Files = os.listdir('\\\\psfiler01\\data\\SurveyReports')


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

all_years_months = ['201405', '201406']

log_files_list = []

for i in range(0, len(all_years_months)):

    for files in Log_Files:
        if "aggregate" in files:
            continue

        elif ".csv" not in files:
            continue

        elif "old" in files:
            continue

        elif all_years_months[i] in files:
            log_files_list.append(files)

header = {0: ['SurveyType', 'VisitorId', 'IP', 'SurveyStartTime', 'ProfileGuid', 'Platform', 'Fingerprint', 'Saw10', 'Bailed10', 'TimeOn10', 'BrowseConfirm10', 'Saw20', 'Bailed20', 'BrowseConfirm20', 'Saw30', 'Bailed30', 'BrowseConfirm30', 'SawMyPayscale', 'Activated', 'Aircraft Type Ratings\Aircraft Type Rating Unprompted', 'AssociateEducation\Major Unprompted', 'BachelorEducation\Major Unprompted', 'BankType\BankType Unprompted', 'Benefits_Perks\Benefits_Perks Unprompted', 'Certifications\Certifications Unprompted', 'EducationValue\EducationValue Unprompted', 'Employer\Employer Name Unprompted', 'Employer\ProductActivity Unprompted', 'Employment Status2\Employment Status Unprompted', 'EstablishmentType\EstablishmentType Unprompted', 'FirstPageSkippable', 'FunTrivia\UnderemployedReason Unprompted', 'Height10', 'Height15', 'Height20', 'Height30', 'Height50', 'Height60', 'Height70', 'Height80', 'HotelRating\OtherRating Unprompted', 'IPGeoTargetCityState', 'IPGeoTargetCityStateAfter', 'IPGeoTargetCountry', 'IPGeoTargetCountryAfter', 'Job\Job Unprompted', 'Job 5 Years Ago\Job Unprompted', 'Language\Language Unprompted', 'Location\City Unprompted', 'Location\State Unprompted', 'Manager Job\Job Unprompted', 'MasterEducation\Major Unprompted', 'MBAEducation\Major Unprompted', 'NoGood', 'PassedInData', 'PhDEducation\Major Unprompted', 'Practice Area\Practice Area Unprompted', 'PrevMilitaryExp\HighestRank Unprompted', 'Primary Responsibilities\Primary Responsibilities Unprompted', 'SawChoose', 'SawSimilarJob', 'Security Clearance\Security Clearance Type Unprompted', 'Skill\Skill Unprompted', 'Subjects Taught\Subject Taught Unprompted', 'Union Memberships\Union Memberships Unprompted', 'Width10', 'Width15', 'Width20', 'Width30', 'Width50', 'Width60', 'Width70', 'Width80', 'Profile ABTest-2013_choosepage_test01', 'Profile ABTest-2013_choosepage_test02', 'Profile ABTest-2013_choosepage_test03', 'Profile ABTest-2013_choosepage_test04', 'Profile ABTest-2013_choosepage_test05', 'Profile ABTest-2013_homepage_test01', 'Profile ABTest-2013_homepage_test02', 'Profile ABTest-2013_homepage_test03', 'Profile ABTest-2013_homepage_test04', 'Profile ABTest-2013_homepage_test05', 'Profile ABTest-2013_homepage_test06', 'Profile ABTest-BrowseConfirmTest', 'Profile ABTest-floating_bar_abtest', 'Profile ABTest-inline-bnc', 'Profile ABTest-InlineBnc-AcTest', 'Profile ABTest-InlineBrowseConfirmTest', 'Profile ABTest-mousetracking', 'Profile ABTest-mrt_test_flow_ultima', 'Profile ABTest-mrt-joinbutton', 'Profile ABTest-notapplicabletest', 'Profile ABTest-offeroptin', 'Profile ABTest-offerviewab', 'Profile ABTest-onmouseoversurveylink01', 'Profile ABTest-popup_designtest', 'Profile ABTest-probabilitycacheanswersearchtest', 'Profile ABTest-rc_bannerad', 'Profile ABTest-rroffershown', 'Profile ABTest-salarycalculatorresultad', 'Profile ABTest-showjoblistingsabovechart', 'Profile ABTest-showspan9addplacementhigh', 'Profile ABTest-showspan9addplacementlow', 'Profile ABTest-SurveyABTest', 'Profile ABTest-surveyemployernameswapwithproductactivitytest', 'Profile ABTest-surveyresponsivetest', 'Profile ABTest-surveystart_designtest', 'Profile ABTest-surveystyletest', 'Profile city', 'Profile country', 'Profile employer', 'Profile hasEmail', 'Profile job', 'Profile job.unprompted', 'Profile profile start type', 'Profile state', 'Profile userid', 'SurveyLevel FastTrack-10', 'SurveyLevel FastTrack-10-Browse-City', 'SurveyLevel FastTrack-10-Browse-Job', 'SurveyLevel FastTrack-10-Browse-State', 'SurveyLevel FastTrack-10-Browse-Years_Experience', 'SurveyLevel FastTrack-10-Confirm-City', 'SurveyLevel FastTrack-10-Confirm-Job', 'SurveyLevel FastTrack-10-Confirm-State', 'SurveyLevel FastTrack-15', 'SurveyLevel FastTrack-15-Browse-Bonus', 'SurveyLevel FastTrack-15-Browse-Hourly-Rate', 'SurveyLevel FastTrack-15-Browse-HourlyWorkWeek', 'SurveyLevel FastTrack-15-Browse-Monthly-Income', 'SurveyLevel FastTrack-15-Browse-Overtime-Rate', 'SurveyLevel FastTrack-15-Browse-Salary', 'SurveyLevel FastTrack-20', 'SurveyLevel FastTrack-20-Browse-Annual-Store-Revenue', 'SurveyLevel FastTrack-20-Browse-BudgetUnderManagement', 'SurveyLevel FastTrack-20-Browse-Certifications', 'SurveyLevel FastTrack-20-Browse-Grade-Taught', 'SurveyLevel FastTrack-20-Browse-Job', 'SurveyLevel FastTrack-20-Browse-Manager-Organization-Size', 'SurveyLevel FastTrack-20-Browse-Physician-Practicing-Status', 'SurveyLevel FastTrack-20-Browse-Skill', 'SurveyLevel FastTrack-20-Browse-Tenured', 'SurveyLevel FastTrack-20-Confirm-Aircraft-Type-Rating', 'SurveyLevel FastTrack-20-Confirm-Certifications', 'SurveyLevel FastTrack-20-Confirm-Job', 'SurveyLevel FastTrack-20-Confirm-Language', 'SurveyLevel FastTrack-20-Confirm-Practice-Area', 'SurveyLevel FastTrack-20-Confirm-Skill', 'SurveyLevel FastTrack-20-Confirm-Subject-Taught', 'SurveyLevel FastTrack-30', 'SurveyLevel FastTrack-30-Browse-CompanyStockExchange', 'SurveyLevel FastTrack-30-Browse-Employer-Name', 'SurveyLevel FastTrack-30-Browse-Employer-Type', 'SurveyLevel FastTrack-30-Browse-ProductActivity', 'SurveyLevel FastTrack-30-Confirm-Employer-Name', 'SurveyLevel FastTrack-30-Confirm-ProductActivity', 'SurveyLevel FastTrack-50', 'SurveyLevel FastTrack-50-Browse-Benefits_Perks', 'SurveyLevel FastTrack-50-Browse-Health-Insurance', 'SurveyLevel FastTrack-50-Confirm-Benefits_Perks', 'SurveyLevel FastTrack-60', 'SurveyLevel FastTrack-60-Browse-Amount-Authorized2', 'SurveyLevel FastTrack-60-Browse-Number-Of-Equity-Partners', 'SurveyLevel FastTrack-60-Browse-Number-Of-Lawyers', 'SurveyLevel FastTrack-60-Browse-Signing-Authority', 'SurveyLevel FastTrack-60-Browse-Union-Memberships', 'SurveyLevel FastTrack-60-Confirm-BankType', 'SurveyLevel FastTrack-60-Confirm-EstablishmentType', 'SurveyLevel FastTrack-60-Confirm-OtherRating', 'SurveyLevel FastTrack-60-Confirm-Security-Clearance-Type', 'SurveyLevel FastTrack-60-Confirm-Union-Memberships', 'SurveyLevel FastTrack-70', 'SurveyLevel FastTrack-70-Browse-HighestRank', 'SurveyLevel FastTrack-70-Browse-Job', 'SurveyLevel FastTrack-70-Browse-Major', 'SurveyLevel FastTrack-70-Confirm-HighestRank', 'SurveyLevel FastTrack-70-Confirm-Job', 'SurveyLevel FastTrack-70-Confirm-Major', 'SurveyLevel FastTrack-80', 'SurveyLevel FastTrack-80-Confirm-EducationValue', 'SurveyLevel FastTrack-80-Confirm-UnderemployedReason', 'SurveyLevel FastTrack-910-Browse-Job', 'SurveyLevel FastTrack-Edit-10', 'SurveyLevel FastTrack-Edit-10-Browse-City', 'SurveyLevel FastTrack-Edit-10-Browse-Job', 'SurveyLevel FastTrack-Edit-10-Browse-State', 'SurveyLevel FastTrack-Edit-10-Confirm-City', 'SurveyLevel FastTrack-Edit-10-Confirm-Job', 'SurveyLevel FastTrack-Edit-15', 'SurveyLevel FastTrack-Edit-15-Browse-HourlyWorkWeek', 'SurveyLevel FastTrack-Edit-20', 'SurveyLevel FastTrack-Edit-20-Browse-Job', 'SurveyLevel FastTrack-Edit-20-Confirm-Certifications', 'SurveyLevel FastTrack-Edit-20-Confirm-Job', 'SurveyLevel FastTrack-Edit-20-Confirm-Practice-Area', 'SurveyLevel FastTrack-Edit-20-Confirm-Skill', 'SurveyLevel FastTrack-Edit-30', 'SurveyLevel FastTrack-Edit-30-Browse-Employer-Name', 'SurveyLevel FastTrack-Edit-30-Browse-ProductActivity', 'SurveyLevel FastTrack-Edit-30-Confirm-Employer-Name', 'SurveyLevel FastTrack-Edit-30-Confirm-ProductActivity', 'SurveyLevel FastTrack-Edit-50', 'SurveyLevel FastTrack-Edit-50-Browse-Health-Insurance', 'SurveyLevel FastTrack-Edit-50-Confirm-Benefits_Perks', 'SurveyLevel FastTrack-Edit-60', 'SurveyLevel FastTrack-Edit-600', 'SurveyLevel FastTrack-Edit-70', 'SurveyLevel FastTrack-Edit-70-Confirm-HighestRank', 'SurveyLevel FastTrack-Edit-70-Confirm-Job', 'SurveyLevel FastTrack-Edit-70-Confirm-Major', 'SurveyLevel FastTrack-Edit-80', 'SurveyLevel JobOffer-10', 'SurveyLevel JobOffer-10-Browse-City', 'SurveyLevel JobOffer-10-Browse-Job', 'SurveyLevel JobOffer-10-Browse-State', 'SurveyLevel JobOffer-10-Browse-Years_Experience', 'SurveyLevel JobOffer-10-Confirm-City', 'SurveyLevel JobOffer-10-Confirm-Job', 'SurveyLevel JobOffer-15', 'SurveyLevel JobOffer-15-Browse-Annual-Profit-Disbursement', 'SurveyLevel JobOffer-15-Browse-Bonus', 'SurveyLevel JobOffer-15-Browse-Hourly-Rate', 'SurveyLevel JobOffer-15-Browse-HourlyWorkWeek', 'SurveyLevel JobOffer-15-Browse-Monthly-Income', 'SurveyLevel JobOffer-15-Browse-Overtime-Rate', 'SurveyLevel JobOffer-15-Browse-Salary', 'SurveyLevel JobOffer-20', 'SurveyLevel JobOffer-20-Browse-Certifications', 'SurveyLevel JobOffer-20-Browse-Grade-Taught', 'SurveyLevel JobOffer-20-Browse-Physician-Practicing-Status', 'SurveyLevel JobOffer-20-Browse-Skill', 'SurveyLevel JobOffer-20-Confirm-Certifications', 'SurveyLevel JobOffer-20-Confirm-Job', 'SurveyLevel JobOffer-20-Confirm-Language', 'SurveyLevel JobOffer-20-Confirm-Practice-Area', 'SurveyLevel JobOffer-20-Confirm-Skill', 'SurveyLevel JobOffer-20-Confirm-Subject-Taught', 'SurveyLevel JobOffer-30', 'SurveyLevel JobOffer-30-Browse-CompanyStockExchange', 'SurveyLevel JobOffer-30-Browse-Employer-Name', 'SurveyLevel JobOffer-30-Browse-Employer-Type', 'SurveyLevel JobOffer-30-Browse-ProductActivity', 'SurveyLevel JobOffer-30-Confirm-Employer-Name', 'SurveyLevel JobOffer-30-Confirm-ProductActivity', 'SurveyLevel JobOffer-50', 'SurveyLevel JobOffer-50-Browse-Health-Insurance', 'SurveyLevel JobOffer-50-Confirm-Benefits_Perks', 'SurveyLevel JobOffer-60', 'SurveyLevel JobOffer-600', 'SurveyLevel JobOffer-60-Browse-Number-Of-Equity-Partners', 'SurveyLevel JobOffer-60-Browse-Number-Of-Lawyers', 'SurveyLevel JobOffer-60-Confirm-BankType', 'SurveyLevel JobOffer-60-Confirm-Security-Clearance-Type', 'SurveyLevel JobOffer-70', 'SurveyLevel JobOffer-70-Browse-HighestRank', 'SurveyLevel JobOffer-70-Browse-Job', 'SurveyLevel JobOffer-70-Browse-Major', 'SurveyLevel JobOffer-70-Confirm-HighestRank', 'SurveyLevel JobOffer-70-Confirm-Job', 'SurveyLevel JobOffer-70-Confirm-Major', 'SurveyLevel JobOffer-80', 'SurveyLevel JobOffer-80-Confirm-Employment-Status', 'SurveyLevel UE-10', 'SurveyLevel UE-10-Browse-City', 'SurveyLevel UE-10-Browse-Job', 'SurveyLevel UE-10-Browse-State', 'SurveyLevel UE-10-Browse-Years_Experience', 'SurveyLevel UE-10-Confirm-City', 'SurveyLevel UE-10-Confirm-Job', 'SurveyLevel UE-10-Confirm-State', 'SurveyLevel UE-20', 'SurveyLevel UE-20-Browse-BudgetUnderManagement', 'SurveyLevel UE-20-Browse-Certifications', 'SurveyLevel UE-20-Browse-Employment-Status', 'SurveyLevel UE-20-Browse-Grade-Taught', 'SurveyLevel UE-20-Browse-Manager-Organization-Size', 'SurveyLevel UE-20-Browse-Physician-Practicing-Status', 'SurveyLevel UE-20-Browse-PIC_Hours', 'SurveyLevel UE-20-Browse-Pilot-Certificate', 'SurveyLevel UE-20-Browse-Practice-Area', 'SurveyLevel UE-20-Browse-Primary-Responsibilities', 'SurveyLevel UE-20-Browse-Skill', 'SurveyLevel UE-20-Browse-Subject-Taught', 'SurveyLevel UE-20-Confirm-Aircraft-Type-Rating', 'SurveyLevel UE-20-Confirm-Certifications', 'SurveyLevel UE-20-Confirm-Employment-Status', 'SurveyLevel UE-20-Confirm-Practice-Area', 'SurveyLevel UE-20-Confirm-Primary-Responsibilities', 'SurveyLevel UE-20-Confirm-Skill', 'SurveyLevel UE-20-Confirm-Subject-Taught', 'SurveyLevel UE-30', 'SurveyLevel UE-30-Browse-CompanySales', 'SurveyLevel UE-30-Browse-CompanyStockExchange', 'SurveyLevel UE-30-Browse-Employer-Name', 'SurveyLevel UE-30-Browse-ProductActivity', 'SurveyLevel UE-30-Confirm-Employer-Name', 'SurveyLevel UE-30-Confirm-ProductActivity', 'SurveyLevel UE-40', 'SurveyLevel UE-40-Browse-Job', 'SurveyLevel UE-40-Confirm-HighestRank', 'SurveyLevel UE-40-Confirm-Job', 'SurveyLevel UE-40-Confirm-Major', 'SurveyLevel UE-Edit-10', 'SurveyLevel UE-Edit-10-Browse-City', 'SurveyLevel UE-Edit-10-Browse-State', 'SurveyLevel UE-Edit-10-Confirm-City', 'SurveyLevel UE-Edit-10-Confirm-Job', 'SurveyLevel UE-Edit-20', 'SurveyLevel UE-Edit-20-Browse-Manager-Organization-Size', 'SurveyLevel UE-Edit-20-Browse-Practice-Area', 'SurveyLevel UE-Edit-20-Browse-Primary-Responsibilities', 'SurveyLevel UE-Edit-20-Browse-Subject-Taught', 'SurveyLevel UE-Edit-20-Confirm-Certifications', 'SurveyLevel UE-Edit-20-Confirm-Employment-Status', 'SurveyLevel UE-Edit-20-Confirm-Primary-Responsibilities', 'SurveyLevel UE-Edit-20-Confirm-Skill', 'SurveyLevel UE-Edit-20-Confirm-Subject-Taught', 'SurveyLevel UE-Edit-30', 'SurveyLevel UE-Edit-30-Browse-Employer-Name', 'SurveyLevel UE-Edit-30-Confirm-Employer-Name', 'SurveyLevel UE-Edit-30-Confirm-ProductActivity', 'SurveyLevel UE-Edit-40', 'SurveyLevel UE-Edit-40-Browse-Job', 'SurveyLevel UE-Edit-40-Confirm-HighestRank', 'SurveyLevel UE-Edit-40-Confirm-Job', 'SurveyLevel UE-Edit-40-Confirm-Major', 'SurveyLevel UE-Edit-600', 'FieldGroupsShownCount', 'CompletedSurvey']}


for files in log_files_list:

    data_list = []

    print "Reading " + files
    with open(Log_Files_Path + files, 'rb') as R:
        reader = csv.reader(R, delimiter=',')
        data_list.extend(reader)

    print "Writing " + files
    with open(Log_Files_Path + files, 'wb') as W:
        writer = csv.writer(W, lineterminator='\n')

        for line, row in enumerate(data_list):
            data = header.get(line, row)
            writer.writerow(data)



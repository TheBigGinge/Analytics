import os
import os.path
import csv
import getpass
import zipfile
import datetime
#import recent_users

localpath = os.path.expanduser("~"+getpass.getuser())+"\\desktop\\"
DataPath = '\\\\filer01\\public\\Data_Analytics\\PSP Log Metrics\\Data Files\\'
ZipPath = '\\\\filer01\\prodlogs\\Zips\\'
IWEB01A = '\\\\insightweb01a\\LogFiles\\VerboseLog\\'
IWEB01B = '\\\\insightweb01b\\LogFiles\\VerboseLog\\'
IWEB02A = '\\\\insightweb03a\\LogFiles\\VerboseLog\\'
IWEB02B = '\\\\insightweb03b\\LogFiles\\VerboseLog\\'
WorkingDir = os.getcwd()


now = str(datetime.datetime.now())
todaysdate = now[:7]
todaysdate = todaysdate.replace('-', '')


'''The ArchZipList is the Archived list of Zip files with only the Verbose logs
from each of the Insight Web machines.'''
ArchZipList = []
ZipDir = os.listdir(ZipPath)

def ZipListAppend():
    for files in ZipDir:
        if 'INSIGHTWEB03A' in files and 'VerboseLog' in files:
            ArchZipList.append(files)
        elif 'INSIGHTWEB01A' in files and 'VerboseLog' in files:
            ArchZipList.append(files)
        elif 'INSIGHTWEB03B' in files and 'VerboseLog' in files:
            ArchZipList.append(files)
        elif 'INSIGHTWEB01B' in files and 'VerboseLog' in files:
            ArchZipList.append(files)
        else:
            continue
print "Appending Files"
ZipListAppend()

CurrentFileList = []

def WebPathAppend(WebPath):
    WebDir = os.listdir(WebPath)
    for files in WebDir:
        if 'JobTitleMatchingV2_' in files:
            CurrentFileList.append(files)
        else:
            continue
        
WebPathAppend(IWEB01A)
WebPathAppend(IWEB01B)
WebPathAppend(IWEB02A)
WebPathAppend(IWEB02B)

ArchZipList.sort()
testlist = []
DaysList = []


def Account_Type_Lookup():
    
    Lookup_Dict = {}
    
    with open(DataPath + 'Account_ID_Lookup.csv','rb') as f:
        reader = csv.reader(f,delimiter=',')
        names = reader.next()
        
        for row in reader:
            Account_ID = row[names.index('PSAccountID')]
            Subscription = row[names.index('Subscription Type')]
            Lookup_Dict[Account_ID] = Subscription
            
    return Lookup_Dict
    
Account_Type_Mapping = Account_Type_Lookup()


class DataPull:
    def __init__(self, rowlist):
        self.rowlist = rowlist
        if len(self.rowlist) >= 16:
            self.QueryCount = None
            self.FindTime()
            self.CreateDate()
            self.FindPosition()
            self.MoreCount()
            self.Search_Term_Grab()
            self.Subscription_Type()
            self.is_internal()
            self.output = self.CreateDate,self.FindPosition,self.QueryCount,self.MoreCount,self.Search_Term_Grab,\
                          self.Subscription_Type, self.is_internal
        else:
            self.output = 'N/A'

    def is_internal(self):
        if "IsCustomer" in self.rowlist:
            self.is_internal = True
        else:
            self.is_internal = False
            
    def FindTime(self):
        for item in self.rowlist:
            if '/' in item and item.find('/') != item.rfind('/') and '0' in item and ":" in item and '-' not in item and item.isalpha() == False and len(item) == 24:
                self.FindTime = item
            
    def CreateDate(self):
        Mon,Day,Year = self.FindTime[0:2], self.FindTime[3:4], self.FindTime[6:10]
        self.CreateDate = Year+'-'+Mon
        
    def FindPosition(self):
        for item in range(0,len(self.rowlist)-1):
            try:
                if isinstance(int(self.rowlist[item]),int) == True and isinstance(int(self.rowlist[item+1]),int) == True:
                    self.FindPosition = self.rowlist[item]
                    self.QueryCount = self.rowlist[item+1]
            except ValueError:
                continue
                    
    def MoreCount(self):
        #TODO: Major bug in the More Count leaving instances of an object in the csv count files
        for item in range(0,len(self.rowlist)-1):
            if self.rowlist[item] == 'Search Result' or self.rowlist[item] == 'Pin title':
                self.MoreCount = self.rowlist[item+1]
            elif self.rowlist[item] == 'default':
                self.MoreCount = self.rowlist[item-1]
                
    def Search_Term_Grab(self):

        for i,item in enumerate(self.rowlist):
            if 'jobmatch-incremental' in item:
                Searches = self.rowlist[i+1].split(',')
                Number_Searches = len(Searches)
                self.Search_Term_Grab = Number_Searches
                
    def Subscription_Type(self):
        
        for i,item in enumerate(self.rowlist):
            if item == 'Information':
                try:
                    Acct_ID = self.rowlist[i+1]
                except IndexError:
                    Acct_ID = None
        try:
            Subs_Type = Account_Type_Mapping[Acct_ID]
        except KeyError:
            Subs_Type = None
        
        self.Subscription_Type = Subs_Type
        


class ZipFileRead:
    def __init__(self, logfiles):
        self.logfiles = logfiles
        if todaysdate in self.logfiles:
            print "Skipping Current Month LogFile. \n"
        else:
            self.testfile = zipfile.ZipFile(ZipPath + logfiles)
            self.filelist = self.testfile.namelist()
            self.JobMatchFile()
            print "Working on " + str(self.JobMatchFile)
            self.extract()
            self.removeFile()
        
    def JobMatchFile(self):
        for f in self.filelist:
            if 'JobTitleMatchingV2' in f:
                self.JobMatchFile = f
                
    def extract(self):
        self.testfile.extract(self.JobMatchFile,WorkingDir)
        self.FileUsed = WorkingDir + '\\' + self.JobMatchFile
        with open(self.FileUsed) as LetsDoThis:
            for row in csv.reader(LetsDoThis,delimiter = ',',quotechar = '"'):
                if len(row) < 16:
                    continue
                else:
                    data = DataPull(row)
                    if data.output[6] is False:
                        testlist.append(data.output)
                        Date = self.JobMatchFile[len('JobTitleMatchingV2_'):len('JobTitleMatchingV2_')+10]
                        Mon,Day,Year = Date[4:6],Date[6:8],Date[0:4]
                        FinalDate = Year + '-' + Mon
                        DaysList.append(FinalDate)
                
    def removeFile(self):
        os.remove(self.FileUsed)

   
for i in range(0,len(ArchZipList)-1):
    try: 
        ZipFileRead(ArchZipList[i])
    except KeyError:
        continue
        
# Remember to csv read these files before pulling data, Ginger!        
'''
for fancy in CurrentFileList:
    fancyData = DataPull(fancy)
    testlist.append(fancyData.output)
    DaysList.append(fancyData.CreateDate)
'''    


AllDatesUsed = list(set(DaysList))



print "Writing Insight to file"
header = ['Date','Find Position','Query Count','More Count','Search Terms']
writer = csv.writer(open(DataPath + "Insight PSP Metrics.csv",'w'),lineterminator='\n')
writer.writerow(header)
for row in testlist:
    if row[5] == 'Insight':
        Date = row[0]
        FinPos = row[1]
        QuCo = row[2]
        MoCo = row[3]
        Search = row[4]
        Final = Date,FinPos,QuCo,MoCo,Search
        writer.writerow(Final)
    else:
        continue
        

print "Writing Market Rate to file"
header = ['Date','Find Position','Query Count','More Count','Search Terms']
writer = csv.writer(open(DataPath + "Market Rate PSP Metrics.csv",'w'),lineterminator='\n')
writer.writerow(header)
for row in testlist:
    if row[5] == 'Market Rate':
        Date = row[0]
        FinPos = row[1]
        QuCo = row[2]
        MoCo = row[3]
        Search = row[4]
        Final = Date,FinPos,QuCo,MoCo,Search
        writer.writerow(Final)
    else:
        continue

print "Writing All PSP to file"
header = ['Date','Find Position','Query Count','More Count','Search Terms']
writer = csv.writer(open(DataPath + "General PSP Metrics.csv",'w'),lineterminator='\n')
writer.writerow(header)
for row in testlist:
    Date = row[0]
    FinPos = row[1]
    QuCo = row[2]
    MoCo = row[3]
    Search = row[4]
    Final = Date,FinPos,QuCo,MoCo,Search
    writer.writerow(Final)

            
print "Program Complete"
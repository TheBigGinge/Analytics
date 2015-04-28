import os
import csv
import datetime
import getpass
import aequitas_functions

now = str(datetime.datetime.now())
todaysdate = now[:7]
todaysdate = todaysdate.replace('-', '')
todaysdateAlt = now[:7]

Year, Month = todaysdateAlt.split('-')

Bad_Report_List = []

#Quarter Dict is used for file titles
Quarter_Dict = {'01': 'Q1', '02': 'Q1', '03': 'Q1', '04': 'Q2', '05': 'Q2', '06': 'Q2', '07': 'Q3', '08': 'Q3',
                '09': 'Q3', '10': 'Q4', '11': 'Q4', '12': 'Q4'}

Write_Date = Quarter_Dict[Month] + ' ' + Year

Report_Path = '\\\\filer01\\DBBACK\\AnalysisToolReports\\Results\\'
Writing_Path = '\\\\filer01\\public\\Data_Analytics\\Aequitas\\' + Write_Date + '\\'
Stored_Files = '\\\\filer01\\public\\Data_Analytics\\Aequitas\\'

print "Gathering XML files from the Analysis Tool \n" 
All_XML_Files = os.listdir(Report_Path)
Overall_XML_Files = ['Ryan Aequitas Overall Start Pay', 'Ryan Aequitas Overall Exp Pay']

print "Pulling all the XML files needed for this analysis \n"
Four_Digit_EXP_Files = aequitas_functions.compile_xml_files(4, 'Exp', All_XML_Files)
Four_Digit_Start_Files = aequitas_functions.compile_xml_files(4, 'Start', All_XML_Files)
Two_Digit_EXP_Files = aequitas_functions.compile_xml_files(2, 'Exp', All_XML_Files)
Two_Digit_Start_Files = aequitas_functions.compile_xml_files(2, 'Start', All_XML_Files)


CIP_Mapping = {}


aequitas_functions.cip_map(CIP_Mapping, 'CIP_Mapping.csv', Stored_Files)
aequitas_functions.cip_map(CIP_Mapping, 'CIP_Mapping_Alt.csv', Stored_Files)
    
IPEDS_Mapping = aequitas_functions.IPEDS_Map(Stored_Files)
    
All_Schools = aequitas_functions.school_list(Stored_Files)
    
School_Majors = aequitas_functions.school_major_list(Stored_Files)


class GatherXmlData:
    
    def __init__(self):

        self.two_dig_start = self.xml_to_dictionary(Two_Digit_Start_Files)
        self.boot_strap_and_write_lists(self.two_dig_start, 'Two Digit Starting Pay.csv')
        self.write_bad_reports(Bad_Report_List)
        self.two_dig_exp = self.xml_to_dictionary(Two_Digit_EXP_Files)
        self.boot_strap_and_write_lists(self.two_dig_exp, 'Two Digit Experienced Pay.csv')
        self.four_dig_start = self.xml_to_dictionary(Four_Digit_Start_Files)
        self.boot_strap_and_write_lists(self.four_dig_start, 'Four Digit Starting Pay.csv')
        self.four_dig_exp = self.xml_to_dictionary(Four_Digit_EXP_Files)
        self.boot_strap_and_write_lists(self.four_dig_exp, 'Four Digit Experienced Pay.csv')
        self.overall_start = self.overall_xml_to_dictionary(Overall_XML_Files[0])
        self.boot_strap_and_write_overall_lists(self.overall_start, 'Overall School Starting Pay.csv')
        self.overall_exp = self.overall_xml_to_dictionary(Overall_XML_Files[1])
        self.boot_strap_and_write_overall_lists(self.overall_exp, 'Overall School Experienced Pay.csv')

    @staticmethod
    def write_bad_reports(bad_report_list):
        
        local_path = os.path.expanduser("~" + getpass.getuser()) + "\\desktop\\"
        
        with open(local_path + 'Bad Reports.csv', 'a') as A:
            writer = csv.writer(A, lineterminator='\n')
            
            for row in bad_report_list:
                writer.writerow(row)

    @staticmethod
    def bad_reports(ipeds, school, cip, major, reason, output_list):
        
        final = ipeds, school, cip, major, reason
        
        output_list.append(final)

    @staticmethod
    def xml_to_dictionary(file_list):
        
        dictionary = {}
        error_count = 0
        
        for CIP_Files in file_list:
            
            print "Pulling data from " + CIP_Files + ' \n'
            
            xml_list = []

            with open(CIP_Files, 'rb') as F:
                [xml_list.append(lines) for lines in F]

            eac_list = []

            school_list = []
            cip_codes = []

            counter = 0

            for i, line in enumerate(xml_list):

                counter += 1
                if counter % 10000 == 0:
                    print '%s lines processed' % counter

                if '<Caption>' in line and '<TableReport' in xml_list[i+1]:
                    cip_code = line[line.find('<Caption>')+len('<Caption>'):line.find('</Caption>')].replace('&amp;',
                                                                                                             '&')
                    cip_codes.append(cip_code)
                    dictionary[cip_code] = {}

                if '<TableReport Name="' in line:
                    school_name = xml_list[i+1][xml_list[i+1].find('<Caption>')+len('<Caption>'):
                                                xml_list[i+1].find('</Caption>')].replace('&amp;', '&')

                if '<Row Name="' in line:
                    eac = xml_list[i+2][xml_list[i+2].find('<Entry>')+len('<Entry>'):xml_list[i+2].find('</Entry>')]
                    eac = float(eac)
                    eac_list.append(eac)

                if '</TableReport>' in line:
                    try:
                        dictionary[cip_code][school_name] = eac_list
                        school_list.append(school_name)
                        eac_list = []
                    except KeyError:
                        error_count += 1
                        print school_name, cip_code, error_count
                        continue

            for schulen in All_Schools:
                if schulen not in school_list:
                    cip = cip_codes[0]
                    dictionary[cip][schulen] = "No Data"
                    
        return dictionary

    @staticmethod
    def overall_xml_to_dictionary(cip_files):

        dictionary = {}
        
        print "Pulling data from " + cip_files + ' \n'
        
        xml_list = []
        
        with open(Report_Path + cip_files + "\\0.xml", 'rb') as F:
            [xml_list.append(lines) for lines in F]

        eac_list = []
        
        school_list = []
        
        counter = 0
        
        for i, line in enumerate(xml_list):
            
            counter += 1
            if counter % 10000 == 0:
                print '%s lines processed' % counter                
                
            if '<TableReport Name="' in line:
                school_name = xml_list[i+1][xml_list[i+1].find('<Caption>')+len('<Caption>'):
                                            xml_list[i+1].find('</Caption>')].replace('&amp;', '&')
                
            if '<Row Name="' in line:
                eac = xml_list[i+2][xml_list[i+2].find('<Entry>')+len('<Entry>'): xml_list[i+2].find('</Entry>')]
                eac = float(eac)
                eac_list.append(eac)
                
            if '</TableReport>' in line:
                dictionary[school_name] = eac_list
                school_list.append(school_name)
                eac_list = []

        return dictionary

    @staticmethod
    def reality_check(ipeds_code, cip_code):
        
        cip_check = cip_code.find('.')

        if cip_check > 0:
            cip_code = cip_code[:cip_code.find('.')]
                
        try:
            count = int(School_Majors[ipeds_code][cip_code])
        except KeyError:
            count = 0
            print cip_code
            
        if count > 0:
            return True            
            
        if count == 0:
            return False

    def boot_strap_and_write_lists(self, dictionary_of_lists, csv_title):
        
        if not os.path.exists(Writing_Path):
            os.makedirs(Writing_Path)   
            
        dict_keys = dictionary_of_lists.keys()
        
        print "Boot Strapping and Writing " + csv_title + " to file"
        
        header = ['IPEDS ID', 'School', 'Major', 'CIP Code', '25th Percentile Pay', 'Median Pay', '75th Percentile Pay',
                  'Confidence Level on the Median', "Report or Don't Report", 'Lower Bound 90% CI(25th)',
                  'Upper Bound 90% CI(25th)', 'Lower Bound 90% CI(50th)', 'Upper Bound 90% CI(50th)',
                  'Lower Bound 90% CI(75th)', 'Upper Bound 90% CI(75th)']
                
        with open(Writing_Path + todaysdateAlt + " " + csv_title, 'wb') as f:
            writer = csv.writer(f, delimiter="|", lineterminator='\n')
            writer.writerow(header)
        
            for i, keys in enumerate(dict_keys):
                print "Boot Strapping the " + keys + " CIP Code"
                counter = 0
                for Schools in dictionary_of_lists[keys]:
                    counter += 1
                    
                    if counter % 50 == 0:
                        print "Bootstrapped %s Schools" % counter
                        
                    ipeds_id = IPEDS_Mapping[Schools]
                    cip_code = keys
                    Major = CIP_Mapping[keys]

                    if self.reality_check(ipeds_id, cip_code) is False:
                        
                        self.bad_reports(ipeds_id, Schools, cip_code, Major, "Reality Check", Bad_Report_List)
                        continue

                    else:
                        
                        twenty_fifth = aequitas_functions.boot_strap(dictionary_of_lists[keys][Schools], 1000, 25)
                        fiftieth = aequitas_functions.boot_strap(dictionary_of_lists[keys][Schools], 1000, 50)
                        seventy_fifth = aequitas_functions.boot_strap(dictionary_of_lists[keys][Schools], 1000, 75)
                        
                        twenty_five, t_f_error, t_f_tenth, t_f_ninetieth, t_f_distance = twenty_fifth
                        median, m_error, m_tenth, m_ninetieth, m_distance = fiftieth
                        seventy_five, s_f_error, s_f_tenth, SFNinetieth, SFDistance = seventy_fifth

                        report = "Don't Report"
                        
                        if m_error in ['Low Data', 'Very Low', 'No Data']:
                            report = "Don't Report"

                        elif m_error not in ['Low Data', 'No Data', 'N/R', 'Very Low']:
                            report = "Report"
                            
                        if m_error == 'No Data':
                            self.bad_reports(ipeds_id, Schools, cip_code, Major, "No Data or less than 5",
                                             Bad_Report_List)
                            continue
                            
                        if m_error == 'N/R':
                            self.bad_reports(ipeds_id, Schools, cip_code, Major, "High Variability", Bad_Report_List)
                            continue

                        if median == twenty_five or median == seventy_five:
                            twenty_five = 'Low Data'
                            seventy_five = 'Low Data'
                            
                        if median == 'No Data':
                            twenty_five = 'No Data'
                            seventy_five = 'No Data'
                            
                        if m_error == 'Low Data':
                            twenty_five = 'Low Data'
                            seventy_five = 'Low Data'

                        final = ipeds_id, Schools, Major, cip_code, twenty_five, median, seventy_five, m_error, \
                                report, t_f_tenth, t_f_ninetieth, m_tenth, m_ninetieth, \
                                s_f_tenth, SFNinetieth
                                
                        writer.writerow(final)

    @staticmethod
    def boot_strap_and_write_overall_lists(dictionary_of_lists, csv_title):
        
        if not os.path.exists(Writing_Path):
            os.makedirs(Writing_Path)   
        
        print "Boot Strapping and Writing " + csv_title + " to file"
        
        header = ['IPEDS', 'School', '25th Percentile Pay', 'Median Pay', '75th Percentile Pay',
                  'Confidence Level on the Median', "Report or Don't Report",'Lower Bound 90% CI(25th)',
                  'Upper Bound 90% CI(25th)', 'Lower Bound 90% CI(50th)','Upper Bound 90% CI(50th)',
                  'Lower Bound 90% CI(75th)','Upper Bound 90% CI(75th)']        
                
        with open(Writing_Path + todaysdateAlt + " " + csv_title, 'wb') as f:
            writer = csv.writer(f, delimiter="|", lineterminator='\n')
            writer.writerow(header)
            
            counter = 0
               
            for Keys in dictionary_of_lists:
                
                counter += 1

                print "Boot Strapping " + Keys + " which is %s of 1055" % counter
                
                Schools = Keys
                
                IPEDS = IPEDS_Mapping[Schools]
                
                Twenty_Fifth = aequitas_functions.boot_strap(dictionary_of_lists[Keys],1000,25)
                Fiftieth = aequitas_functions.boot_strap(dictionary_of_lists[Keys],1000,50)
                Seventy_Fifth = aequitas_functions.boot_strap(dictionary_of_lists[Keys],1000,75)
                            
                
                Twenty_Five, TFerror, TFTenth, TFNinetieth, TFDistance = Twenty_Fifth
                Median, Merror, MTenth, MNinetieth, MDistance = Fiftieth
                Seventy_Five, SFerror, SFTenth, SFNinetieth, SFDistance = Seventy_Fifth
                
                if Merror in ['Low Data','Very Low']:
                    Report = "Don't Report"
                    
                if Merror in ['No Data','N/R']:
                    continue

                if Merror not in ['Low Data','No Data','N/R','Very Low']:
                    Report = "Report"             

                if Median == Twenty_Five or Median == Seventy_Five:
                    Twenty_Five = 'Low Data'
                    Seventy_Five = 'Low Data'
                    
                if Median == 'No Data':
                    Twenty_Five = 'No Data'
                    Seventy_Five = 'No Data'    
                    
                if Merror == 'Low Data':
                    Twenty_Five = 'Low Data'
                    Seventy_Five = 'Low Data'        

                Final = IPEDS, Schools, Twenty_Five, Median, Seventy_Five, Merror, Report, TFTenth, TFNinetieth, MTenth, \
                        MNinetieth, SFTenth, SFNinetieth
                        
                writer.writerow(Final)

GatherXmlData()
                    
                    
print "Program is complete"
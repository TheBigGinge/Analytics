import csv
import numpy as np
import random as rd
import os

#Pulls all of the XML valid XML files from the Analysis Tool and puts them in a list


def compile_xml_files(digits, experience_range, all_files):
    report_path = '\\\\filer01\\dbback\\AnalysisToolReports\\Results\\'
    file_list = []
    fill = None
    number = None
    
    if digits == 4:
        number = 'Four'
        fill = ' New'
    elif digits == 2:
        number = 'Two'
        fill = ''
        
    for files in all_files:
        if 'Ryan Aequitas ' + number + ' Dig ' + experience_range + ' Pay' + fill in files:
            for xml_files in os.listdir(report_path + files + "\\"):
                if 'Main' not in xml_files:
                    file_list.append(report_path + files + "\\" + xml_files)
            
    return file_list
    
## End of XML_List Compiling -----------------------------------------------------------------------------------------##

##Excel Files suck so this CIP Mapping has to make up for the loss of leading and trailing 0's


def cip_map(map_dict, file_name, path):
    
    """Just dealing with my excel files removing leading and trailing 0's
    Also dealing with .'s being removed for numbers like 20.00"""
    
    with open(path + file_name, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        names = reader.next()
        
        for row in reader:
            major = row[names.index('Major')]
            id = row[names.index('ID')]
            id_length = len(id)

            first = None
            second = None
            
            if file_name == 'CIP_Mapping_Alt.csv':
            
                if id_length == 1:
                    id = "0" + id
                    
                elif id_length == 2:
                    id = id
                
                map_dict[id] = major

            elif file_name == 'CIP_Mapping.csv':
            
                if id_length < 5:
                    check = id.split('.')
                    
                    if len(check) == 1:
                        
                        if id_length == 1:
                            id = "0" + id + ".00"
                            
                        elif id_length == 2:
                            id += ".00"
                            
                    elif len(check) == 2:
                        
                        if len(check[0]) == 1:
                            first = "0" + check[0]
                            
                        if len(check[0]) == 2:
                            first = check[0]
    
                        if len(check[1]) == 1:
                            second = check[1] + "0"
                            
                        if len(check[1]) == 2:
                            second = check[1]

                        id = first + "." + second

                map_dict[id] = major

##End of CIP_Map -----------------------------------------------------------------------------------------------------##

##Main Bootstrapping Function


def boot_strap(input_list, repeats, percentile):
    
    """Doesn't return actual variance but verbage for pre-defined ranges
    The ranges were adjusted for the second version of this package"""

    percent_list = []
    n = len(input_list)
    
    if "No Data" in input_list:
        final = 'No Data', 'No Data', 'No Data', 'No Data', 'No Data'
        return final
        
    elif n < 5:
        overall_percentile = np.percentile(input_list, percentile)
        final = int(round(overall_percentile, -2)), 'Low Data', 'Low Data', 'Low Data', 'Low Data'
        return final
        
    elif n >= 5:
                
        overall_percentile = np.percentile(input_list, percentile)
        
        result = [None] * n
        for x in xrange(repeats):
            for i in xrange(n):
                j = int(rd.random() * n)
                result[i] = input_list[j]
            percent_list.append(np.percentile(result, percentile))
            
        tenth = np.percentile(percent_list, 10)
        ninetieth = np.percentile(percent_list, 90)
        
        distance_a = abs((overall_percentile - tenth) / tenth)
        distance_b = abs((overall_percentile - ninetieth) / ninetieth)
        possibles = [distance_a, distance_b]
        distance = max(possibles)

        error = None
        
        if distance < .10:
            error = "High"
        elif .10 <= distance < .2:
            error = "Medium"
        elif .3 > distance >= .2:
            error = "Low"
        elif .6 > distance >= .3:
            error = "Very Low"
        elif distance >= .6:
            error = "N/R"
            
        final = int(round(overall_percentile, -2)), error, int(round(tenth, -2)), int(round(ninetieth, -2)), \
            int(round(distance, -2))
        
        return final

##End Bootstrap ------------------------------------------------------------------------------------------------------##


##School Name to IPEDS dictionary
def IPEDS_Map(File_Path):

    Map_Dict = {}
    
    with open(File_Path + 'IPEDS_Mapping.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        names = reader.next()
        for row in reader:
            school = row[names.index('School Name')]
            ID = row[names.index('IPEDS')]
            Map_Dict[school] = ID
            
    return Map_Dict

##End IPEDS MAP ------------------------------------------------------------------------------------------------------##


#All schools used for the report put into a list
def school_list(file_path):
  
    school_return_list = []
    
    with open(file_path + 'IPEDS_Mapping.csv','rb') as f:
        reader = csv.reader(f, delimiter=',')
        names = reader.next()
        for row in reader:
            school = row[names.index('School Name')]
            school_return_list.append(school)
            
    return school_return_list

##End School List ----------------------------------------------------------------------------------------------------##


#Creates a dictionary for all School Majors
def school_major_list(file_path):
    
    return_dictionary = {}
    
    with open(file_path + 'Three_Year_Completions_Counts.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        names = reader.next()
         
        cip_list = []
        
        for Numbers in names:
            if 'UnitID' in Numbers or 'Institution Name' in Numbers:
                continue
            else:
                cip_list.append(Numbers)

        for row in reader:
            ipeds = row[names.index('UnitID')]
            return_dictionary[ipeds] = {}
            
            for keys in cip_list:
                check = len(keys)
                
                if check == 1:
                    full_cip = "0" + keys
                    return_dictionary[ipeds][full_cip] = row[names.index(keys)]
                
                else:
                    return_dictionary[ipeds][keys] = row[names.index(keys)]

    return return_dictionary

school_major_list('\\\\filer01\\public\\Data_Analytics\\Aequitas\\')
    
##End School Major List ----------------------------------------------------------------------------------------------##
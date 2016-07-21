import AnalysisTool.extract_data_xml as extract
import os
import AnalysisTool.deserialize_xml as my_xml

anon_out = "\\\\filer02\\public\\Data_Analytics\\AnonReports\\TempOut\\"

class AlumniDTO:

    def __init__(self):
        self.query_01 = {}
        self.query_02 = {}
        self.query_03 = {}
        self.query_04 = {}
        self.query_05 = {}
        self.query_06 = {}

test = AlumniDTO()

for xml_files in os.listdir(anon_out):
    if ".xml" in xml_files and 'Gina Alumni Analytics Query 1' in xml_files:
        my_xml.fix_xml_encoding(anon_out, xml_files)


    if 'Gina Alumni Analytics Query 4' in xml_files and '.xml' in xml_files:
        data_dict = extract.ExtractXMLData(anon_out + xml_files).table_def_medians_list_handler()
        main_key = 'Gina %s Query 04' % 1234
        if main_key not in test.query_01.keys():
            test.query_01[main_key] = data_dict
        else:
            copy_dict = test.query_01[main_key]
            copy_dict.update(data_dict)
            test.query_01[main_key] = copy_dict

print test.query_01
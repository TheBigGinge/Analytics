import xml
import os
import AnalysisTool.deserialize_xml as extract
import AnalysisTool.deserialize_xml as xml_parse
import KaylaBot.QuestionDashboard.gui_code_behind as cb


class RowNameEntryHandler(xml.sax.ContentHandler):

    """
    Used for parsing the Analysis Tool xml files.

    Here's how to call this class:

    with report_handler(UNCModelCountContentHandler) as handler:
        with open(infile, 'rb') as ifh:
            xml.sax.parse(ifh, handler)

        job_count_dictionary = handler.count_dictionary
    Returns:
        Dictionary with Key = str() and value = float()
    """

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.count_dictionary = {}
        self.date_count_dictionary = {}
        self.date = None
        self.title_header = None
        self.position = 0
        self.counter = 0
        self.first = True
        self.file_count = 0
        self.elements = []
        self.row_name = ''
        self.entry_value = ''

    def elem_str(self):
        return '/'.join(self.elements)

    def startElement(self, name, attrs):
        self.elements.append(name)

        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Row':
            self.position = 1
            self.row_name = attrs.get('Name')

        if elem_str == 'Reports/TableReport/Row/Entry':
            self.entry_value = ''

    def endElement(self, name):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Row':
            self.row_name = ''

        if elem_str == 'Reports/TableReport/Row/Entry':
            if self.row_name in self.count_dictionary.keys():
                pass
            else:
                self.count_dictionary[self.row_name] = float(self.entry_value)

                try:
                    self.date_count_dictionary[self.date][self.row_name] = self.entry_value
                except KeyError:
                    self.date_count_dictionary[self.date] = {}
                    self.date_count_dictionary[self.date][self.row_name] = self.entry_value

        # unwind part of the stack so the other event handlers know where they are
        if self.elements and self.elements[-1] == name:
            self.elements.pop()

    def characters(self, content):
        elem_str = self.elem_str()

        if elem_str == 'Reports/Caption':
            self.title_header = content

        if elem_str == 'Reports/TableReport/Row/Entry':
            self.entry_value = content

        if elem_str == 'Reports/Caption':
            self.date = content


class ExtractXMLData:

    def __init__(self, infile):
        self.infile = infile

    def overall_data_count(self):
        with xml_parse.report_handler(extract.OverallDataCount) as handler:
            with open(self.infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            return handler.count_dictionary

    def row_name_entry_handler(self, header=False):
        with xml_parse.report_handler(extract.RowNameEntryHandler) as handler:
            with open(self.infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            if header is True:
                return handler
            else:
                return handler.count_dictionary

    def overall_medians_list_return(self):
        with xml_parse.report_handler(extract.OverallMediansListReturn) as handler:
            with open(self.infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            return handler.median_dictionary

    def iqr_content_handler(self):

        with xml_parse.report_handler(extract.NameIQRContentHandler) as handler:
            with open(self.infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            return handler.count_dictionary

    def model_content_handler(self):

        with xml_parse.report_handler(extract.NameModelCountContentHandler) as handler:
            with open(self.infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            return handler.count_dictionary

    def fix_xml_encoding(self, file_path):
        """
        Currently the Analysis Tool is spitting out xml files with utf-16 encoding when it should
        be utf-8. So, you need to use this to change the designation.
        """

        with open(file_path + self.infile, 'rb') as original:
            with open(file_path + "Temp File.txt", 'wb') as temp:
                [temp.write(row.replace("utf-16", "utf-8")) for row in original]

        os.remove(file_path + self.infile)

        with open(file_path + "Temp File.txt", 'rb') as temp:
            with open(file_path + self.infile, 'wb') as new:
                [new.write(row) for row in temp]

        os.remove(file_path + "Temp File.txt")


xml_handler = ExtractXMLData("\\\\filer01\\public\\Data_Analytics\\Answer Conversion Activation and Bail Rates\\"
                      "output_files\\Kayla Question Activation Counts_88.xml").row_name_entry_handler(header=True)

numerator_dict = {}

for question in cb.QuestionDashSupport().get_all_the_questions():
    question = question.replace("/", "_").replace(" ", "_").replace("-", "_")
    numerator_dict[question] = {}

for key_value in xml_handler.count_dictionary:

    question = xml_handler.title_header.replace("/", "_").replace(" ", "_").replace("-", "_")
    onet = key_value[key_value.find("/PayScale Code ") + len("/PayScale Code "):].strip()
    target_count = xml_handler.count_dictionary[key_value]
    numerator_dict[question][onet] = target_count

for key_value in numerator_dict['Hourly_Rate_HourlyWorkWeek'].keys():

    print key_value


import xml.sax
import os
from contextlib import contextmanager


def fix_xml_encoding(file_path, xml_file):
    """
    Currently the Analysis Tool is spitting out xml files with utf-16 encoding when it should
    be utf-8. So, you need to use this to change the designation.
    """

    with open(file_path + xml_file, 'rb') as original:
        with open(file_path + "Temp File.txt", 'wb') as temp:
            [temp.write(row.replace("utf-16", "utf-8")) for row in original]

    os.remove(file_path + xml_file)

    with open(file_path + "Temp File.txt", 'rb') as temp:
        with open(file_path + xml_file, 'wb') as new:
            [new.write(row) for row in temp]

    os.remove(file_path + "Temp File.txt")


@contextmanager
def report_handler(target_class):

    try:
        handler = target_class()
        yield handler
    except Exception as ex:
        print "An error occurred while trying to pull data from the xml file: "
        print ex.message
        raise SystemExit


def clean(s):
    """
    Return a copy of C{s} with spaces, backslashes, and forward slashes
    replaced with underscores.
    """
    return s.replace(' ', '_').replace('\\', '_').replace('/', '_')


class OverallDataCount(xml.sax.ContentHandler):

    """
    Used for parsing the Analysis Tool xml files.
    Creates a dictionary for the AnswerValues and their counts.
    Use Ryan Data Dashboard Job Rollup Counts 2_0.xml as reference.

    Here's how to call this class:

    with report_handler(OverallDataCount) as handler:
        with open(infile, 'rb') as ifh:
            xml.sax.parse(ifh, handler)

        job_count_dictionary = handler.count_dictionary
    Returns:
        Dictionary with Key = str() and value = int()
    """

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.count_dictionary = {}
        self.position = 0
        self.counter = 0
        self.file_count = 0
        self.elements = []
        self.row_name = ''
        self.buffer = ''
        self.counts = None
        self.title = None

    def elem_str(self):
        return '/'.join(self.elements)

    def startElement(self, name, attrs):
        self.elements.append(name)

        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.position = 1
            self.buffer = ""
            self.title = name

        if elem_str == 'Reports/TableReport/Count':
            self.counts

    def endElement(self, name):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.position = 0

        if elem_str == 'Reports/TableReport/Count':
            self.count_dictionary[self.buffer] = int(self.counts)

        # unwind part of the stack so the other event handlers know where they are
        if self.elements and self.elements[-1] == name:
            self.elements.pop()

    def characters(self, content):
        elem_str = self.elem_str()
        if elem_str == 'Reports/TableReport/Caption':
            if self.position:
                self.buffer += content

        if elem_str == 'Reports/TableReport/Count':
            self.counts = content


class NameIQRContentHandler(xml.sax.ContentHandler):

    """
    Used for parsing the Analysis Tool xml files.
    Creates a dictionary for the AnswerValues and their counts.
    Use Ryan Data Dashboard IQR US PayScale Main_0.XML as reference.

    Args:
        Here's how to call this class:

        with report_handler(NameIQRContentHandler) as handler:
            with open(infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            job_count_dictionary = handler.count_dictionary
    Returns:
        Dictionary with Key = str() and value = int()
    """

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.count_dictionary = {}
        self.position = 0
        self.counter = 0
        self.file_count = 0
        self.elements = []
        self.row_name = ''
        self.buffer = ''
        self.iqr = None

    def elem_str(self):
        return '/'.join(self.elements)

    def startElement(self, name, attrs):
        self.elements.append(name)

        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.position = 1
            self.buffer = ""

        if elem_str == 'Reports/TableReport/Row/Entry':
            self.iqr

    def endElement(self, name):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Row/Caption':
            self.position = 0

        if elem_str == 'Reports/TableReport/Row/Entry':
            self.count_dictionary[self.buffer] = float(self.iqr)

        # unwind part of the stack so the other event handlers know where they are
        if self.elements and self.elements[-1] == name:
            self.elements.pop()

    def characters(self, content):
        elem_str = self.elem_str()
        if elem_str == 'Reports/TableReport/Caption':
            if self.position:
                self.buffer += content

        if elem_str == 'Reports/TableReport/Row/Entry':
            self.iqr = content


class NameModelCountContentHandler(xml.sax.ContentHandler):

    """
    Used for parsing the Analysis Tool xml files.
    Creates a dictionary for the AnswerValues and their counts.
    Use Ryan Data Dashboard Jobs with Model US_0.XML as reference.

    Args:
        Here's how to call this class:

        with report_handler(NameModelCountContentHandler) as handler:
            with open(infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            job_count_dictionary = handler.count_dictionary
    Returns:
        Dictionary with Key = str() and value = int()
    """

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.count_dictionary = {}
        self.position = 0
        self.counter = 0
        self.file_count = 0
        self.elements = []
        self.row_name = ''
        self.job_title = ''
        self.iqr = None

    def elem_str(self):
        return '/'.join(self.elements)

    def startElement(self, name, attrs):
        self.elements.append(name)

        elem_str = self.elem_str()

        if elem_str == 'Reports/TextReport/TableReport/Row':
            self.position = 1
            self.job_title = attrs.get('Name')

        if elem_str == 'Reports/TextReport/TableReport/Row/Entry':
            self.iqr

    def endElement(self, name):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TextReport/TableReport/Row':
            self.job_title = ''

        if elem_str == 'Reports/TextReport/TableReport/Row/Entry':
            self.count_dictionary[self.job_title] = float(self.iqr)

        # unwind part of the stack so the other event handlers know where they are
        if self.elements and self.elements[-1] == name:
            self.elements.pop()

    def characters(self, content):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TextReport/TableReport/Row/Entry':
            self.iqr = content


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


class OverallMediansListReturn(xml.sax.ContentHandler):

    def __init__(self):
        """
        Pulls the 10th, 25th, 50th, 75th, and 90th percentiles from Analysis Tool
        files.

        Works for OverallTableDefinition reports that uses medians as the columns drop down

        Example:

        with report_handler(OverallEACMediansListReturn) as handler:
            with open("\\\\psstats03\\reports\\Results\\Ryan Data Dist Week by Week EAC Medians_0.xml", 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            my_dictionary = handler.median_dictionary
        :return:
            A dictionary of lists. The lists being the percentiles listed above.
        """
        self.median_dictionary = {}
        self.eac_list = []
        self.elements = []
        self.row_name = ''
        self.position = 0
        self.list_create = 0

    def elem_str(self):
        return '/'.join(self.elements)

    def startElement(self, name, attrs):
        self.elements.append(name)

        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.row_name = ''
            self.position = 1

        if elem_str == 'Reports/TableReport/Row':
            self.eac_list = []
            self.list_create = 1

    def endElement(self, name):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.position = 0

        if elem_str == 'Reports/TableReport/Row':
            self.list_create = 0
            self.eac_list.pop(0)
            self.eac_list.pop(0)
            self.median_dictionary[self.row_name] = self.eac_list

        # unwind part of the stack so the other event handlers know where they are
        if self.elements and self.elements[-1] == name:
            self.elements.pop()

    def characters(self, content):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            if self.position:
                self.row_name += content

        if elem_str == 'Reports/TableReport/Row/Entry':
            if self.list_create:
                self.eac_list.append(content)



class TableDefinitionMediansListReturn(xml.sax.ContentHandler):

    def __init__(self):

        self.median_dictionary = {}
        self.eac_list = []
        self.elements = []
        self.title = ''
        self.row_name = ''
        self.position = 0
        self.list_create = 0
        self.sep_name = ''
        self.sep = 0

    def elem_str(self):
        return '/'.join(self.elements)

    def startElement(self, name, attrs):
        self.elements.append(name)

        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.row_name = ''
            self.position = 1

        if elem_str == 'Reports/TableReport/Row':
            self.eac_list = []
            self.list_create = 1
            self.sep_name = ''
            self.sep_name = attrs['Name']

    def endElement(self, name):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.position = 0

        if elem_str == 'Reports/TableReport/Row':
            self.list_create = 0
            self.sep = 0
            if self.row_name not in self.median_dictionary[self.title].keys():
                self.median_dictionary[self.title][self.row_name] = {}
            self.median_dictionary[self.title][self.row_name][self.sep_name] = self.eac_list

        # unwind part of the stack so the other event handlers know where they are
        if self.elements and self.elements[-1] == name:
            self.elements.pop()

    def characters(self, content):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            if self.position:
                self.row_name += content

        if elem_str == 'Reports/TableReport/Row/Entry':
            if self.list_create:
                self.eac_list.append(content)

        if elem_str == 'Reports/Caption':
            self.title += content
            self.median_dictionary[self.title] = {}


class SampleDefinitionAlumniAnalytics(xml.sax.ContentHandler):
    def __init__(self):

        self.item_dictionary = {}
        self.eac_list = []
        self.elements = []
        self.title = ''
        self.row_name = ''
        self.position = 0
        self.list_create = 0
        self.sep_name = ''
        self.sep = 0

    def elem_str(self):
        return '/'.join(self.elements)

    def startElement(self, name, attrs):
        self.elements.append(name)

        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.row_name = ''
            self.position = 1

        if elem_str == 'Reports/TableReport/Row':
            self.eac_list = []
            self.list_create = 1
            self.sep_name = ''
            self.sep_name = attrs['Name']

    def endElement(self, name):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            self.position = 0

        if elem_str == 'Reports/TableReport/Row':
            self.list_create = 0
            self.sep = 0
            if self.row_name not in self.item_dictionary[self.title].keys():
                self.item_dictionary[self.title][self.row_name] = {}
            self.item_dictionary[self.title][self.row_name][self.sep_name] = self.eac_list

        # unwind part of the stack so the other event handlers know where they are
        if self.elements and self.elements[-1] == name:
            self.elements.pop()

    def characters(self, content):
        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Caption':
            if self.position:
                self.row_name += content

        if elem_str == 'Reports/TableReport/Row/Entry':
            if self.list_create:
                self.eac_list.append(content)

        if elem_str == 'Reports/TableReport/Row/String':
            if self.list_create:
                self.eac_list.append(content)

        if elem_str == 'Reports/Caption':
            self.title += content
            self.item_dictionary[self.title] = {}
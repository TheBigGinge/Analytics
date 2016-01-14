import deserialize_xml as extract
import xml
import AnalysisTool.deserialize_xml as xml_parse
import os


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

    def table_def_medians_list_handler(self):
        with xml_parse.report_handler(extract.TableDefinitionMediansListReturn) as handler:
            with open(self.infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            return handler.median_dictionary

    def sample_def_alumni_analytics_handler(self):
        with xml_parse.report_handler(extract.SampleDefinitionAlumniAnalytics) as handler:
            with open(self.infile, 'rb') as ifh:
                xml.sax.parse(ifh, handler)

            return handler.item_dictionary

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
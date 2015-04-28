import DateFunctions.datetimes_in as df
import csv


class SplunkSupport:

    def __init__(self):
        self.file_path = '\\\\filer01\\public\\Data_Analytics\\Splunk_PSP_Metrics\\Data\\'
        self.dates = df.DateTimeFormats()

    def augment_splunk_file(self, ):

        with open(self.file_path + str(self.dates.return_today_as_y_m("")) + " Splunk_PSP_Logs.csv", 'rb') as R:
            reader = csv.reader(R, delimiter=',')

            header = reader.next()

            for row in reader:
                query_string = row[header.index("AllQueries")]
                query_list = query_string.split(",")
                query_length = len(query_list)




SplunkSupport().augment_splunk_file()

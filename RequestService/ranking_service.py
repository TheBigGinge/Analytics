import csv
import requests
import time


class RankingService:

    def __init__(self, input_file, out_dir):
        self.out_dir = out_dir
        self.input_File = input_file
        self.host = 'http://phoenix.dc.pssea.office'
        self.port = ':80'
        self.path = '/R/ws2.R'
        self.headers = {'Content-Type': 'multipart/form-data'}

    def rank_request(self):

        response = requests.post(self.host + self.port + self.path,
                                 data=open(self.input_File, 'rb'))

        if response.status_code == 200:
            print "Successful pull. Writing to file \n"
            with open(self.out_dir + 'rankingResults.tsv', 'wb') as W:
                writer = csv.writer(W, delimiter='\t')
                for chunks in response.iter_content(1000):
                    line = chunks.split('\n')

                    for item in line:
                        final = item.split('\t')
                        writer.writerow(final)
            return True
        else:

            print "Something went wrong with ranking service pull. You'll need to try again"
            print "Status code: " + str(response.status_code)
            return False


class PythonRankingService:

    def __init__(self, input_file, out_dir):
        self.out_dir = out_dir
        self.input_File = input_file
        self.host = 'http://phoenix'
        self.port = ':8080'
        #self.headers = {'Content-Type': 'multipart/form-data'}

    def rank_request(self):
        data = open(self.input_File, 'rb')
        start = time.time()
        response = requests.post(self.host + self.port, data=data.read())

        end = time.time()
        print (end - start)
        if response.status_code == 200:
            print "Successful pull. Writing to file \n"
            with open(self.out_dir + 'rankingResults.tsv', 'wb') as W:
                writer = csv.writer(W, delimiter='\t')
                for chunks in response.iter_content(10240):
                    line = chunks.split('\n')

                    for item in line:
                        final = item.split('\t')
                        writer.writerow(final)
            return True
        else:

            print "Something went wrong with ranking service pull. You'll need to try again"
            print "Status code: " + str(response.status_code)
            return False

PythonRankingService("\\\\filer01\\public\\Data_Analytics\\JobMatcher\\OutData\\input.tsv",
                     "C:\\users\\ryanm\\desktop\\").rank_request()
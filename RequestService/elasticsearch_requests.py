import requests
import xml.etree.ElementTree as ET
import csv


class ElasticRequest:

    def __init__(self, search_item, industry, out_dir):
        self.industry = industry
        self.file_name = 'input.tsv'
        self.out_dir = out_dir
        self.search_item = search_item
        self.host = 'psbuilder05b.dc.pssea.office'
        self.method = 'GET'
        self.port = ':86'
        self.uri = '/answersearch/answersearch.asmx/SearchAllWithRollup'
        self.job_title_query = '?answerValue=' + self.search_item + '&rollupSet=PSPJobRollup&' \
                                                                    'fieldName=Job&minFrequency=1' \
                                                                    '&maxMatches=100&useProbabilityCache=false'

    def call_elasticsearch(self):
        response = requests.get('http://' + self.host + self.port + self.uri + self.job_title_query)
        results = ET.fromstring(response.text)
        return results

    def call_elasticsearch_test(self):
        response = requests.get('http://' + self.host + self.port + self.uri + self.job_title_query)
        results = ET.fromstring(response)
        return results

    def jobs_results_to_dictionary(self):

        xml_dict = {}
        root = self.call_elasticsearch()
        for child in root:
            title_match = child.find('{http://www.payscale.com/webservices/AnswerSearch}Text').text
            #profile_id = child.find('{http://www.payscale.com/webservices/AnswerSearch}ID').text
            profile_id = 1
            frequency = child.find('{http://www.payscale.com/webservices/AnswerSearch}Frequency').text
            score = child.find('{http://www.payscale.com/webservices/AnswerSearch}Score').text
            xml_dict[title_match] = {'profile_id': profile_id, 'frequency': frequency, 'score': score}


        return xml_dict

    def job_results_to_dictionary_test(self):

        root = self.call_elasticsearch()
        for child in root:
            print child.find('{http://www.payscale.com/webservices/AnswerSearch}Text').text
            print child.find('{http://www.payscale.com/webservices/AnswerSearch}ID').text
            print child.find('{http://www.payscale.com/webservices/AnswerSearch}Frequency').text
            print child.find('{http://www.payscale.com/webservices/AnswerSearch}Score').text

    def job_results_to_tsv_location(self):

        elastic_results = self.jobs_results_to_dictionary()

        header = ['RollupSearchResult', 'InternalTitle', 'Industry', 'AccountID', 'ProfileID', 'Frequency',
                  'ResultRank', 'Score']

        result_rank = 0
        with open(self.out_dir + self.file_name, 'wb') as W:
            writer = csv.writer(W, delimiter='\t', lineterminator='\n')

            writer.writerow(header)

            for key in elastic_results:
                main = elastic_results[key]
                line = key, self.search_item, 'Software Development', -1, \
                    main['profile_id'], main['frequency'], result_rank, \
                    main['score']

                writer.writerow(line)
                result_rank += 1
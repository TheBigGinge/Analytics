import csv
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import json
import requests

master_file_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\"
master_file = "testSetLexical_DeDupedWithJDs.tsv"
data_path = "C:\\Users\\ryanm\\Documents\\GitHub\\jobmatcher\\data\\"
task_file = "jobtasks.csv"
out_path = "c:\\users\\ryanm\\desktop\\"


def get_descriptions(base_64_file_location, host, idx):
    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "file_location": {
                            "query": base_64_file_location
                        }
                    }
                }
            }
        }
    }
    es_query = json.dumps(query)
    uri = host + '/' + idx + '/_search'
    response = requests.post(uri, data=es_query)
    results = json.loads(response.text)
    skills = []

    skills = []
    try:
        skills = results['hits']['hits'][0]['_source']['full_text']
    except Exception:

        return skills

    return skills

print "Writing data to file"
with open(master_file_path + master_file, 'rb') as R:
    reader = csv.reader(R, delimiter='\t')

    names = reader.next()

    unique_code = 0
    for row in reader:
        company = row[names.index("CompanyName")]
        industry = row[names.index("Industry")]
        internal = row[names.index("InternalTitle")]
        encoded_desc = row[names.index("JobDescription")]
        matched_rollup = row[names.index("MatchedRollup")]
        job_desc = get_descriptions(encoded_desc, "http://novelist:9200", "job_descriptions")
        print job_desc

import RequestService.elasticsearch_requests as er
import RequestService.ranking_service as rs
import csv
import re

#temp_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\TempData\\"
#out_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\OutData\\"

out_path = "c:\\users\\ryanm\\desktop\\"

header = ["Unique_ID", "Twin_Job_Title", "Rollup (0 -2)",
          "NAICS4",
          "ResultRank", "Score"]
calls_made = 0

class OutPut:
    def __init__(self):
        self.top_result = None
        self.score = None
        self.final = None



def get_top_elastic_ranking():
    with open(out_path + "input.tsv", 'rb') as R:
        reader = csv.reader(R, delimiter='\t')
        header = reader.next()
        object_list= []

        for row in reader:

            top_result = row[header.index("RollupSearchResult")]
            result_rank = row[header.index("ResultRank")]
            score = row[header.index("Score")]
            final = top_result, result_rank, score
            temp_object = OutPut()
            temp_object.top_result = top_result
            temp_object.score = score
            temp_object.final = final
            object_list.append(temp_object)

        object_list.sort(key=lambda x: x.score, reverse=True)
        return object_list[:3]


with open("C:\\users\\ryanm\\desktop\\MissingEntries.tsv", 'rb') as r:
    reader = csv.reader(r, delimiter='\t')
    with open("C:\\users\\ryanm\\desktop\\EquifaxResultsFifteen.csv", 'ab') as gnw:
        writer = csv.writer(gnw, delimiter=",")

        #writer.writerow(header)
        reader.next()

        counter = 0
        for entry in reader:

            internal_title = entry[1]
            industry_used = entry[3]
            unique_code = entry[0]
            if int(unique_code) <= 0:
                continue
            else:

                er.ElasticRequest(internal_title,
                                  industry_used,
                                  out_path).job_results_to_tsv_location()

                calls_made += 1
                print "working on id %s..." % unique_code
                print "----------next----------"

                results = get_top_elastic_ranking()

                for i in xrange(0, len(results)):

                    line = unique_code, internal_title, results[i].final[0], industry_used, i, results[i].final[2]

                    writer.writerow(line)


import RequestService.elasticsearch_requests as er
import RequestService.ranking_service as rs
import csv

temp_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\TempData\\"
out_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\OutData\\"

header = ["Job Code", "Job Title", "PayScale Title",
          "LM-Industry",
          "ResultRank", "T"]
calls_made = 0



def get_top_ranking():

    with open(out_path + "rankingResults.tsv", 'rb') as R:
        reader = csv.reader(R, delimiter='\t')
        header = reader.next()

        for row in reader:
            top_result = row[header.index("RollupSearchResult")]
            result_rank = row[header.index("ResultRank")]
            t = row[header.index("T")]
            final = top_result, result_rank, t


def get_top_elastic_ranking():
    with open(out_path + "input.tsv", 'rb') as R:
        reader = csv.reader(R, delimiter='\t')
        header = reader.next()

        for row in reader:
            top_result = row[header.index("RollupSearchResult")]
            result_rank = row[header.index("ResultRank")]
            score = row[header.index("Score")]
            final = top_result, result_rank, score
            return final

with open("C:\\users\\ryanm\\desktop\\ADP_Data_09_2015.csv", 'rb') as r:
    reader = csv.reader(r, delimiter=',')
    with open(temp_path + "FinalStuff.csv", 'wb') as gnw:
        writer = csv.writer(gnw, delimiter=",")

        writer.writerow(header)
        reader.next()

        counter = 0
        for entry in reader:


            internal_title = entry[6]
            industry_used = entry[11]
            unique_code = int(entry[0])
            er.ElasticRequest(internal_title,
                              industry_used,
                              out_path).job_results_to_tsv_location()

            check = rs.PythonRankingService(out_path + "input.tsv",
                                      out_path).rank_request()
            calls_made += 1
            print "%s calls made..." % calls_made
            print "----------next----------"
            if check is True:

                results = get_top_ranking()
                line = unique_code, internal_title, results[0], industry_used, results[1], results[2]

                writer.writerow(line)
            else:
                continue
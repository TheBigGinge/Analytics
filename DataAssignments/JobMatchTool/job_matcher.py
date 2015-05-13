import csv
import random
import RequestService.elasticsearch_requests as er
import RequestService.ranking_service as rs
import RequestService.jd_request as jr
import SqlTools.postgres_heroku as ph
import RyanBot.DataDashboard.dashboard_support as ds


master_file_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\"
master_file = "testSetLexical_DeDupedWithJDs_forMatchTest.tsv"
test_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\TestData\\"
out_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\OutData\\"
temp_path = "\\\\filer01\\public\\Data_Analytics\\JobMatcher\\TempData\\"

data_path = "C:\\Users\\ryanm\\Documents\\GitHub\\jobmatcher\\data\\"
task_file = "jobtasks.csv"


print "Gathering all tasks.."
all_tasks = ds.DashboardSupport().create_deduped_task_dictionary()


def get_top_ranking():

    with open(out_path + "rankingResults.tsv", 'rb') as R:
        reader = csv.reader(R, delimiter='\t')
        header = reader.next()

        for row in reader:
            top_result = row[header.index("RollupSearchResult")]
            result_rank = row[header.index("ResultRank")]
            t = row[header.index("T")]
            final = top_result, result_rank, t
            return final


def create_out_files_create_db_table(file_name, header, entry_list, main_dict):
    calls_made = 0

    postgres = ph.PostgresHeroku()
    conn_string = "host=ec2-23-23-199-181.compute-1.amazonaws.com dbname=d9g290r40m5d9p port=5432 " + \
                  "user=pgfffwsqctjvtd password=hjTE-HRs9fzpnyAGq-YgJohQ2a"

    create_string = '''CREATE TABLE pfaa (Job_Code text, Job_Title text, PayScale_Title text, Match_Code text,
    job_description text, LM_Industry text, Tasks text, RollupSearchResult text, ResultRank text, T text,
    RollupTasks text)'''

    postgres.set_conn_string_from_string(conn_string)
    postgres.authenticate()
    postgres.sql_command('''DROP TABLE pfaa''')
    postgres.sql_command(create_string)

    with open(temp_path + file_name, 'wb') as gnw:
        writer = csv.writer(gnw, delimiter=",")

        writer.writerow(header)

        for entry in entry_list:
            calls_made += 1
            print "%s calls made..." % calls_made
            print "----------next----------"
            line = main_dict[entry]
            internal_title = line[1]
            industry_used = line[5]
            er.ElasticRequest(internal_title,
                              industry_used,
                              out_path).job_results_to_tsv_location()

            check = rs.RankingService(out_path + "input.tsv",
                                      out_path).rank_request()

            if check is True:

                results = get_top_ranking()
                try:
                    search_tasks = all_tasks[results[0].lower()]
                except KeyError:
                    search_tasks = [""]

                short_search_string = create_task_string(search_tasks)
                line.append(results[0])
                line.append(results[1])
                line.append(results[2])
                line.append(short_search_string)

                insert_string = '''INSERT INTO pfaa VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}',
                '{9}','{10}')'''.format(line[0], line[1], line[2], line[3], line[4].replace("'", "''"),
                                        line[5], line[6].replace("'", "''"), line[7], line[8],
                                        line[9], line[10].replace("'", "''"))

                postgres.sql_command(insert_string)

                writer.writerow(line)
            else:
                continue

    postgres.commit_and_close()

    print "Calls completed..."

#storing all answers with a random key and then
#using rand function to sample randomly back
#into the dictionary
gnw_jds = {}


def create_task_string(task_list):

    first = True
    final_task = None
    for task in task_list:
        if first is True:
            final_task = task
            first = False
        else:
            final_task += " " + task

    return final_task

possible_entries = []

print "Splitting up data..."
with open(test_path + master_file, 'rb') as R:
    reader = csv.reader(R, delimiter='\t')

    names = reader.next()

    unique_code = 0
    for row in reader:
        company = row[names.index("CompanyName")]
        industry = row[names.index("Industry")]
        industry = industry[:industry.find("\\")]
        internal = row[names.index("InternalTitle")]
        encoded_desc = row[names.index("JobDescription")]
        matched_rollup = row[names.index("MatchedRollup")]
        job_desc = jr.get_descriptions(encoded_desc, "http://novelist:9200", "job_descriptions")
        try:
            short_tasks = all_tasks[matched_rollup.lower()]
        except KeyError:
            short_tasks = [""]

        short_task_string = create_task_string(short_tasks)

        ppfa_gnw_jds_row = [unique_code, internal, matched_rollup, "PS-CharlesMaxwellScofieldBoyd", job_desc,
                            industry, short_task_string]

        gnw_jds[unique_code] = ppfa_gnw_jds_row

        possible_entries.append(unique_code)

        unique_code += 1
        if unique_code == 93:
            break

print "Choosing a random sample..."
entries_to_use = random.sample(xrange(len(possible_entries)), len(possible_entries))

print "Writing to file..."
create_out_files_create_db_table("pfaa-gnw-jds.csv", ["Job Code", "Job Title", "PayScale Title", "Match Code",
                                                      "job description", "LM-Industry", "Tasks", "RollupSearchResult",
                                                      "ResultRank", "T", "SearchTasks"],
                                 entries_to_use, gnw_jds)

print "Complete"
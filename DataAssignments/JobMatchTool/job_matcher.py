import csv
import json
import requests
import random

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
    try:
        skills = results['hits']['hits'][0]['_source']['full_text']
    except Exception:

        return skills

    return skills


def get_payscale_tasks():
    task_dict = {}

    with open(data_path + task_file, 'rb') as R:
        reader = csv.reader(R, delimiter='\t')
        names = reader.next()

        for row in reader:
            title = row[names.index("JobRollup")].lower()
            task = row[names.index("Task")]

            if title not in task_dict.keys():
                task_dict[title] = []
                task_dict[title].append(task)
            else:
                task_dict[title].append(task)

    return task_dict


def create_out_files(file_name, header, entry_list, main_dict):
    with open(out_path + file_name, 'wb') as gnw:
        writer = csv.writer(gnw, delimiter=",")

        writer.writerow(header)

        for entry in entry_list:
            line = main_dict[entry]
            writer.writerow(line)

#Dictionaries for each file
gnw_jds = {}
gnw = {}
gnw_auto = {}

print "Gathering all tasks.."
all_tasks = get_payscale_tasks()


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
with open(master_file_path + master_file, 'rb') as R:
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
        job_desc = get_descriptions(encoded_desc, "http://novelist:9200", "job_descriptions")
        try:
            short_tasks = all_tasks[matched_rollup.lower()]
        except KeyError:
            short_tasks = [""]

        short_task_string = create_task_string(short_tasks)

        ppfa_gnw_row = unique_code, internal, matched_rollup, "PS-Kari"
        ppfa_gnw_jds_row = unique_code, internal, job_desc, industry, short_task_string
        ppfa_gnw_auto_row = unique_code, internal, matched_rollup, "PS-Kari"

        gnw[unique_code] = ppfa_gnw_row
        gnw_jds[unique_code] = ppfa_gnw_jds_row
        gnw_auto[unique_code] = ppfa_gnw_auto_row

        possible_entries.append(unique_code)

        unique_code += 1

print "Choosing a random sample..."
entries_to_use = random.sample(possible_entries, 100)

print "Writing to file..."
create_out_files("pfaa-gnw-jds.csv", ["Job Code", "Job Title", "job description", "LM-Industry", "Tasks"],
                 entries_to_use, gnw_jds)
create_out_files("ppfa_gnw.csv", ["Job Code", "Job Title", "PayScale Title", "Match Code"], entries_to_use, gnw)
create_out_files("ppfa_gnw-auto.csv", ["Job Code", "Job Title", "PayScale Title", "Score"], entries_to_use, gnw_auto)

print "Complete"
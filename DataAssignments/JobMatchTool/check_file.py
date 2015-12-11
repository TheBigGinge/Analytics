import csv

row_check = {}
key_set = set()
naics_combo = set()
missing = set()

class PullDupes:

    def run_it(self):
        with open('c:\\users\\ryanm\\desktop\\PAYSCALE_job_titles.tsv', 'rb') as R:
            with open('c:\\users\\ryanm\\desktop\\EquifaxResults_cleaned.csv', 'rb') as RA:
                with open('c:\\users\\ryanm\\desktop\\Equifax_Dupes.csv', 'wb') as W:
                    writer = csv.writer(W, lineterminator="\n", delimiter=",")
                    reader_alt = csv.reader(RA, delimiter=',')
                    reader = csv.reader(R, delimiter='\t')
                    header = ['Twin_Job_Title', 'NAICS4', 'id']
                    writer.writerow(header)
                    reader.next()
                    reader_alt.next()

                    for row in reader_alt:
                        title = row[0]
                        key_set.add(title)

                    print len(key_set)

                    for item in reader:
                        job = item[0]
                        naics = item[1]
                        id = item[2]

                        if job in key_set:
                            line = job, naics
                            if line not in  naics_combo:
                                new_line = job, naics, id
                                writer.writerow(new_line)
                                naics_combo.add(new_line)

        print "complete"


class FindJobsForProCompRange:
    def run_it(self):
        with open('c:\\users\\ryanm\\desktop\\EquifaxResultsFinal.tsv', 'rb') as R:
            with open('c:\\users\\ryanm\\desktop\\ProCompJobsAlt.tsv', 'wb') as W:
                reader = csv.reader(R, delimiter='\t')
                writer = csv.writer(W, lineterminator='\n', delimiter='\t')
                reader.next()

                for row in reader:
                    job = row[2]
                    key_set.add(job)

                for item in key_set:
                    line = item, ""
                    writer.writerow(line)

class FindMissingEntries:
    def run_it(self):
        with open('c:\\users\\ryanm\\desktop\\PAYSCALE_job_titles.tsv', 'rb') as R:
            with open('c:\\users\\ryanm\\desktop\\EquifaxResultsAll.csv', 'rb') as RA:
                with open('c:\\users\\ryanm\\desktop\\MissingEntries.tsv', 'wb') as W:
                    writer = csv.writer(W, lineterminator='\n', delimiter='\t')
                    reader = csv.reader(R, delimiter='\t')
                    reader_alt = csv.reader(RA, delimiter=',')

                    reader.next()
                    reader_alt.next()

                    for row in reader_alt:
                        id = row[0]
                        key_set.add(id)

                    for item in reader:
                        check_id = item[2]
                        if check_id not in key_set:
                            missing.add(check_id)
                            line = check_id, ""
                            writer.writerow(item)


class RemoveNoMatch:
    def run_it(self):
        last_line = []
        with open('c:\\users\\ryanm\\desktop\\EquifaxResultsMissing.csv', 'rb') as R:
            with open('c:\\users\\ryanm\\desktop\\EquifaxResultsSecondAlt.csv', 'wb') as W:
                reader = csv.reader(R, delimiter=',')
                writer = csv.writer(W, lineterminator='\n', delimiter=',')

                for row in reader:
                    if row[2] == "No Match":
                        continue
                    else:
                        last_line = []
                        last_line.append(row[0])
                        writer.writerow(row)

        print last_line


class EquifaxResults:
    def __init__(self):
        self.result_one = None
        self.result_two = None
        self.result_three =None


class CombineResults:
    def run_it(self):
        main_dict = {}
        alt_dict = {}

        main_dict_keys = set()
        alt_dict_keys = set()

        with open('c:\\users\\ryanm\\desktop\\EquifaxResultsAll.csv', 'rb') as R:
            with open('c:\\users\\ryanm\\desktop\\EquifaxResultsMissing.csv', 'rb') as RA:
                with open('c:\\users\\ryanm\\desktop\\PAYSCALE_job_titles.tsv', 'rb') as M:
                    with open('c:\\users\\ryanm\\desktop\\EquifaxResultsFinal.tsv', 'wb') as W:
                        counter = 0
                        reader = csv.reader(R, delimiter=',')
                        reader.next()
                        reader_alt = csv.reader(RA, delimiter=',')
                        main_reader = csv.reader(M, delimiter='\t')
                        main_reader.next()

                        writer = csv.writer(W, lineterminator='\n', delimiter='\t')
                        header = ['Unique_ID', 'Twin_Job_Title', 'Rollup (0 -2)', 'NAICS4', 'ResultRank', 'Score']
                        writer.writerow(header)

                        for row in reader:
                            if row[0] in main_dict_keys:
                                main_dict[row[0]].append(row)
                            else:
                                main_dict[row[0]] = []
                                main_dict[row[0]].append(row)
                                main_dict_keys.add(row[0])

                        for line in reader_alt:
                            if line[0] in alt_dict_keys:
                                alt_dict[line[0]].append(line)
                            else:
                                alt_dict[line[0]] = []
                                alt_dict[line[0]].append(line)
                                alt_dict_keys.add(line[0])

                        for item in main_reader:
                            key = item[2]
                            viewable_key = int(key)
                            if viewable_key % 10000 == 0:
                                print 'working on %s...', viewable_key

                            if key in main_dict_keys:
                                target_list = main_dict[key]
                                [writer.writerow(line_to_write) for line_to_write in target_list]

                            elif key in alt_dict_keys:
                                target_list = alt_dict[key]
                                [writer.writerow(line_to_write) for line_to_write in target_list]
                            else:
                                line_to_write = key, item[0], 'No Match', item[1], 'No Match', 'No Match'
                                writer.writerow(line_to_write)


class AddPayPredictions:
    def run_it(self):
        with open('c:\\users\\ryanm\\desktop\\EquifaxResultsFinal.tsv', 'rb') as R:
            with open('c:\\users\\ryanm\\desktop\\all_pro_predictions.tsv', 'rb') as RA:
                with open('c:\\users\\ryanm\\desktop\\ExecCheck.csv', 'rb') as RB:
                    with open('c:\\users\\ryanm\\desktop\\EquifaxResultsFinalPay.tsv', 'wb') as W:
                        comp_dict = {}
                        comp_keys = set()
                        exec_check = set()

                        reader = csv.reader(R, delimiter='\t')
                        reader_alt = csv.reader(RA, delimiter='\t')
                        reader_balt = csv.reader(RB, delimiter=',')
                        writer = csv.writer(W, lineterminator='\n', delimiter='\t')

                        reader.next()
                        reader_alt.next()
                        reader_balt.next()

                        header = ['Unique_ID', 'Twin_Job_Title', 'Rollup (0 -2)', 'NAICS4', 'ResultRank', 'Score',
                                  '10th', '90th', 'Executive Flag']

                        writer.writerow(header)

                        for row in reader_alt:
                            comp_dict[row[0]] = row
                            comp_keys.add(row[0])

                        [exec_check.add(item[3]) for item in reader_balt]

                        for line in reader:
                            id = line[0]
                            internal = line[1]
                            job = line[2]
                            naics = line[3]
                            result = line[4]
                            score = line[5]
                            final = None

                            if job in comp_keys:
                                ten = comp_dict[job][1]
                                ninety = comp_dict[job][5]
                                if job in exec_check:
                                    final = id, internal, job, naics, result, score, ten, ninety, 'true'
                                else:
                                    final = id, internal, job, naics, result, score, ten, ninety, 'false'

                                writer.writerow(final)

                            else:
                                if job in exec_check:
                                    final = id, internal, job, naics, result, score, 'No Data', 'No Data', 'true'
                                else:
                                    final = id, internal, job, naics, result, score, 'No Data', 'No Data', 'false'

                                writer.writerow(final)

with open('c:\\users\\ryanm\\desktop\\EquifaxResultsFinalPay.tsv', 'rb') as R:
    with open('c:\\users\\ryanm\\desktop\\MissingEntriesForKatieSinceSheCantOpenFiles.tsv', 'wb') as W:
        reader = csv.reader(R, delimiter='\t')
        writer = csv.writer(W, delimiter='\t', lineterminator='\n')

        header = ['Unique_ID', 'Twin_Job_Title', 'Rollup (0 -2)', 'NAICS4', 'ResultRank', 'Score',
                  '10th', '90th', 'Executive Flag']

        writer.writerow(header)

        [writer.writerow(row) for row in reader if 'No Match' in row]



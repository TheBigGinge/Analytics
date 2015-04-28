from LogFileTools import log_iterator
import datetime
import csv

csv_logs = log_iterator.CSVLogIterator(datetime.date(2013, 5, 1), datetime.date(2014, 5, 1),
                                       path_to_use="\\\\filer01\\public\\Data Dashboards\\PSP Reports\\")
csv_logs.find_all_logs_dashboard()
csv_rows = csv_logs.iterate_files_return_row()

storage_dict = {}


def pull_final_data(key, sub_key, pa):

    final = key, sub_key, pa
    return final

row_counter = 0
for row in csv_rows:

    if row_counter % 10000 == 0 and row_counter != 0:
        print '%s rows processed' % row_counter

    account_id = row[csv_logs.header.index("Acct ID")]
    product_activity = row[csv_logs.header.index("Product Activity")]
    industry_affinity = row[csv_logs.header.index("Industry Affinity")]
    job = row[csv_logs.header.index("Job")]

    row_counter += 1

    if account_id not in storage_dict.keys():
        storage_dict[account_id] = {}
        storage_dict[account_id][job] = {}
        storage_dict[account_id][job][product_activity] = 1
    elif job not in storage_dict[account_id].keys():
        storage_dict[account_id][job] = {}
        storage_dict[account_id][job][product_activity] = 1
    elif product_activity not in storage_dict[account_id][job].keys():
        storage_dict[account_id][job][product_activity] = 1
    else:
        storage_dict[account_id][job][product_activity] += 1

with open('C:\\users\\ryanm\\desktop\\2014-06 PSP Log PA File.csv', 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    header = ['Account ID', 'Job Title', 'Product Activity', 'Frequency']
    writer.writerow(header)

    for keys in storage_dict.keys():
        sub_key_list = storage_dict[keys].keys()
        for sub_keys in sub_key_list:
            pa_list = storage_dict[keys][sub_keys].keys()
            for pa in pa_list:
                final = keys, sub_keys, pa, storage_dict[keys][sub_keys][pa]
                writer.writerow(final)
                #[writer.writerow(pull_final_data(keys, sub_keys, pa))for pa in pa_list]

print "Program Complete"
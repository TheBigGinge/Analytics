import PSPMetrics
import csv
import sys

print "Finding all log files..."
metrics = PSPMetrics.PSPMetrics()
metrics.find_job_matching_files()
metrics.cycle_zip_files()
sys.path.append("C:\\hg\\payscale\\users\\ryanm\\PayScaleAnalytics\\")


def write_data_to_file(data, file_name, account_type, account_type_alt=None):
    if account_type_alt is None:
        print "Writing " + account_type + " to file"
        header = ['Date', 'Find Position', 'Query Count', 'More Count', 'Search Terms']
        with open(metrics.data_path + file_name, 'wb') as W:
            writer = csv.writer(W, lineterminator='\n')

            writer.writerow(header)
            for row in data:
                if row[5] == account_type and row[1] is not None and row[2] is not None:
                    date = row[0]
                    fin_pos = row[1]
                    query_count = row[2]
                    more_count = row[3]
                    number_searches = row[4]
                    final = date, fin_pos, query_count, more_count, number_searches
                    writer.writerow(final)
                else:
                    continue
    else:
        print "Writing overall data to file"
        header = ['Date', 'Find Position', 'Query Count', 'More Count', 'Search Terms']
        with open(metrics.data_path + file_name, 'wb') as W:
            writer = csv.writer(W, lineterminator='\n')

            writer.writerow(header)
            for row in data:
                if row[1] is not None and row[2] is not None:
                    date = row[0]
                    fin_pos = row[1]
                    query_count = row[2]
                    more_count = row[3]
                    number_searches = row[4]
                    final = date, fin_pos, query_count, more_count, number_searches
                    writer.writerow(final)


write_data_to_file(metrics.is_internal_data, "Insight PSP Metrics IsInternal.csv", 'Insight')
write_data_to_file(metrics.is_customer_data, "Insight PSP Metrics IsCustomer.csv", 'Insight')
write_data_to_file(metrics.is_internal_data, "Market Rate PSP Metrics IsInternal.csv", 'Market Rate')
write_data_to_file(metrics.is_customer_data, "Market Rate PSP Metrics IsCustomer.csv", 'Market Rate')
write_data_to_file(metrics.is_internal_data, "General PSP Metrics IsInternal.csv", 'Insight', 'Market Rate')
write_data_to_file(metrics.is_customer_data, "General PSP Metrics IsCustomer.csv", 'Insight', 'Market Rate')

print "Program Complete"

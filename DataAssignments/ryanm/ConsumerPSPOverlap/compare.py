import csv

breadth_10_dict = {}

with open('C:\\Users\\ryanm\\Desktop\\Main\\Analyses\\2014\\Comsumer vs PSP Data\\consumer_data_40.csv', 'rb') as R:
    reader = csv.reader(R, delimiter=',')

    header = reader.next()

    for i, row in enumerate(reader):
        job = row[header.index("Job")]
        breadth_10 = row[header.index("Industry Breadth 40")]

        if job not in breadth_10_dict.keys():
            breadth_10_dict[job] = set()
            breadth_10_dict[job].add(breadth_10)
        else:
            breadth_10_dict[job].add(breadth_10)


with open('C:\\Users\\ryanm\\Desktop\\Main\\Analyses\\2014\\Comsumer vs PSP Data\\2014-06 PSP Log PA File.csv', 'rb') as R:
    reader = csv.reader(R, delimiter=',')

    header = reader.next()

    with open('C:\\Users\\ryanm\\Desktop\\Main\\Analyses\\2014\\Comsumer vs PSP Data\\OutFile.csv', 'wb') as W:
        writer = csv.writer(W, lineterminator='\n')

        writer_header = ['Account ID', 'Job Title', 'Rollup', 'Product Activity', 'Frequency', 'NAICS 10', 'Match']
        writer.writerow(writer_header)

        for row in reader:

            job = row[header.index("Job Rollup")]
            naics_10 = row[header.index("NAICS 40")]

            try:
                naics_10_list = breadth_10_dict[job]
                if naics_10 in naics_10_list:
                    match = "Match"
                else:
                    match = "No Match"

            except KeyError:
                match = "No Match"

            final = row[0], row[1], job, row[3], row[4], naics_10, match

            writer.writerow(final)
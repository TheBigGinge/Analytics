import csv
import os
import getpass
import Statistics.jaccard_index as stat
import Statistics.entropy as stat_alt


all_employers = []

local_path = os.path.expanduser("~" + getpass.getuser()) + "\\desktop\\"
with open(local_path + "AllEmployees.csv", 'rb') as R:
    reader = csv.reader(R, delimiter=',')

    [all_employers.append(str(row[0])) for row in reader]

all_employers = list(set(all_employers))
length = len(all_employers)

measured = 0

with open("C:\\users\\ryanm\\desktop\\Employer Matching.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    header = ['Employer Name', 'Second Employer Name', 'Entropy Score']

    writer.writerow(header)

    for i in range(0, len(all_employers) - 1):

        print 'Finding jaccard on employer %s of %s total employers' % (i + 1, length)
        for x in range(0, len(all_employers) - 1):
            if i != x:
                try:
                    score = stat.jaccard_index(all_employers[i + measured], all_employers[x + measured])
                    if float(score) > .8:
                        final = all_employers[i + measured], all_employers[x + measured], score
                        writer.writerow(final)
                except IndexError:
                    continue

        measured += 1
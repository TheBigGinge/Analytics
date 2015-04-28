import FileHandling.file_work as fw
import collections as coll
import csv
import sys

"""Quick and dirty script to create a probability cache from the unpropmted files"""
csv.field_size_limit(sys.maxsize)
handler = fw.FileHandler()

matched_list = []
dual_list = []

dual_count = None
single_count = None

#Find the overall file length
file_length = 0
with open("C:\\users\\ryanm\\desktop\\unprompted_2014-06-23.dat", 'rb') as R:
    reader = csv.reader(R, delimiter='\t')

    for row in reader:
        file_length += 1

#Read in the file and count instances intermittently to keep from memory overload
count = 0
with open("C:\\users\\ryanm\\desktop\\unprompted_2014-06-23.dat", 'rb') as R:
    reader = csv.reader(R, delimiter='\t')

    for row in reader:
        count += 1
        if count % 100000 == 0:
            print "%s lines processed..." % count

        if count == 1000000:
            print "Intermediate Counting..."
            dual_count = coll.Counter(dual_list)
            single_count = coll.Counter(matched_list)
            matched_list = []
            dual_list = []

        if count % 1000000 == 0 and count != 1000000 and count != file_length:
            print "Intermediate Counting..."
            temp_dual = coll.Counter(dual_count)
            temp_single = coll.Counter(single_count)

            dual_count = dual_count + temp_dual
            single_count = single_count + temp_single
            matched_list = []
            dual_list = []

        try:
            typed = row[0].lower()
            chosen = row[1].lower()
            if typed != "" and chosen != "":
                matched_list.append(chosen)
                combo = chosen, typed
                dual_list.append(combo)
        except:
            continue

        if count == file_length:
            print "Intermediate Counting..."
            temp_dual = coll.Counter(dual_count)
            temp_single = coll.Counter(single_count)

            dual_count = dual_count + temp_dual
            single_count = single_count + temp_single

#Write results to file
with open("C:\\users\\ryanm\\desktop\\ProbabilityCache.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    header = ['Selected', 'Typed', 'Probability']
    writer.writerow(header)

    for keys in dual_count:

        single = single_count[keys[0]]
        matched = dual_count[keys]

        probability = float(matched) / float(single)

        final = keys[0], keys[1], probability
        writer.writerow(final)
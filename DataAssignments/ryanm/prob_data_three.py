import FileHandling.file_work as fw
import collections as coll
import csv
import nltk
handler = fw.FileHandler()


print "Re-writing main file..."
write_header = True
row_count = 0
with open("C:\\users\\ryanm\\desktop\\test.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    for line in handler.open_csv("C:\\users\\ryanm\\desktop\\truth_data_with_basesalary_comparisons.csv"):
        row_count += 1

        if row_count % 10 == 0:
            print "Processed %s rows...." % row_count

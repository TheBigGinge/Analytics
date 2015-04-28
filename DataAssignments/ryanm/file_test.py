import FileHandling.file_work as fw
import numpy as np
handler = fw.FileHandler()
import csv
import os

file_dir = r"\\filer01\public\Data_Analytics\Aequitas\Q1 2015"


for files in os.listdir(file_dir):
    with open(file_dir + "\\" + files, 'rb') as R:
        with open("C:\\users\\ryanm\\desktop\\Lydia_Aquitas\\" + files, 'wb') as W:
            reader = csv.reader(R, delimiter="|")
            writer = csv.writer(W, lineterminator='\n')

            for row in reader:
                writer.writerow(row)
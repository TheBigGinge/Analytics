

with open("C:\\users\\ryanm\\desktop\\DeVry_Dim.txt", 'rb') as R:

    for line in R:
        header = line[line.find("AS[") + len("AS["):line.find("]")]
        line = line[line.find("]"):]
        while True:
            new_line = line[line.find("AV{School\\School Name\\") + len("AV{School\\School Name\\"):]
import csv

import DateFunctions.date_functions as df


with open("C:\\users\\ryanm\\big_fancy_file\\out.txt", 'rb') as R:
    with open("C:\\users\\ryanm\\big_fancy_file\\fixed_dates.txt", 'wb') as W:

        reader = csv.reader(R, delimiter=',')
        writer = csv.writer(W, delimiter=',', lineterminator='\n')

        header = reader.next()
        writer.writerow(header)

        for i, row in enumerate(reader):
            row_index = header.index("ActivityDateTime")

            test_date = row[row_index]

            formatted_date = df.DateFunctions().rob_date_return(test_date)

            row[row_index] = formatted_date

            writer.writerow(row)




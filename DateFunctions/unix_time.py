import datetime
import time
import csv


start_date = datetime.datetime(2014, 9, 1)

with open("C:\\users\\ryanm\\desktop\\Unix_Times.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    for lines in range(0, 20):

        if lines <= 20:

            new_date = start_date+datetime.timedelta(days=lines)
            first_date = time.mktime(new_date.timetuple())
            second_date = new_date+datetime.timedelta(days=lines+1)
            final_second_date = time.mktime(second_date.timetuple())

            final = first_date, final_second_date, new_date.strftime("%Y-%m-%d")
            writer.writerow(final)

        else:
            break
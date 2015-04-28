import csv

target_path = "c:\\users\\ryanm\\desktop\\Main\\Analyses\\2015\\LAM Score\\"

print "Re-writing file"
with open(target_path + "TwoYearSplunk_2015_03.csv", 'rb') as R:
    with open(target_path + "ConfirmedOutput.csv", 'wb') as W:
        reader = csv.reader(R, delimiter=',')
        writer = csv.writer(W, lineterminator='\n')

        header = reader.next()

        for row in reader:
            created = row[header.index('Created')]
            account_id = row[header.index('AccountID')]
            account_name = row[header.index('AccountName')]
            sfid = row[header.index('SalesForceID')]
            sub_type = row[header.index('SubscriptionType')]
            event = row[header.index('EventName')]
            email = row[header.index('Email')]

            final = created, account_id, account_name, sfid, sub_type, event, email
            writer.writerow(final)

print "finished"
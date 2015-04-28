import csv

with open("c:\\users\\ryanm\\desktop\\UpdatedSplunk_2015_02.csv", 'rb') as R:
    with open("c:\\users\\ryanm\\desktop\\splunk_login_2015_02.csv", 'wb') as W:
        reader = csv.reader(R, delimiter=',')
        writer = csv.writer(W, lineterminator='\n')

        write_header = ['Created', 'AccountID', 'AccountName', 'SalesForceAccountID', 'SubscriptionType',
                        'EventName', 'Email']
        header = reader.next()
        writer.writerow(write_header)

        print "Re-writing file..."
        for row in reader:
            created = row[header.index("Created")]
            accountID = row[header.index("AccountID")]
            account_name = row[header.index("AccountName")]
            sales_force_account_id = row[header.index("SalesForceID")]
            subscription_type = row[header.index("SubscriptionType")]
            event_name = row[header.index("EventName")]
            email = row[header.index("Email")]

            final = created, accountID, account_name, sales_force_account_id, subscription_type, event_name, email
            writer.writerow(final)

print "Completed"
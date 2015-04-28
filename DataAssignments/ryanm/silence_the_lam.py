import csv


class LamSilencing:

    def __init__(self, file_path=None, file_name=None):
        if file_path is None:
            self.file_path = '\\\\filer01\\public\\RobJ\\LAM\\'
        else:
            self.file_path = file_path

        if file_name is None:
            self.file_name = '9-27-14-2yr-log.csv'
        else:
            self.file_name = file_name
        self.header = None
        self.mapping_dict = {}
        self.create_mapping()

    def create_mapping(self):
        print "Creating mapping dictionary..."

        with open("C:\\users\\ryanm\\desktop\\2014-10-01 Cleaned SFIDs.csv", 'rb') as R:
            reader = csv.reader(R, delimiter=',')

            header = reader.next()

            for row in reader:
                account_id = row[header.index("account_id")]
                sfid = row[header.index("sfid")]

                self.mapping_dict[account_id] = sfid

    def read_file(self):

        with open(self.file_path + self.file_name, 'rb') as R:
            reader = csv.reader(R, delimiter=',')

            self.header = reader.next()

            for row in reader:
                yield row

    def find_and_fix_missing_values(self):

        print "Fixing missing values..."

        with open(self.file_path + 'SFID_FIXED.csv', 'wb') as W:
            writer = csv.writer(W, lineterminator='\n')

            header = ['AccountID', 'AccountName', 'AccountGuid', 'AccountSFId', 'SubscriptionType',
                      'SubExpiration', 'ActivityType', 'ActivityDateTime', 'ProfileType', 'ProfileGuid'
                      'UserId', 'Email', 'UserIsInternal']

            writer.writerow(header)

            for row in self.read_file():

                current_sfid = row[self.header.index("AccountSFId")]
                account_id = row[self.header.index("AccountID")]

                if current_sfid == "":
                    try:
                        row[self.header.index("AccountSFId")] = self.mapping_dict[account_id]
                    except KeyError:
                        row[self.header.index("AccountSFId")] = "No SFID"

                    writer.writerow(row)
                else:
                    writer.writerow(row)

        print "Completed"

#create_file = LamSilencing()
#create_file.find_and_fix_missing_values()

accounts = {}
print "Finding emails..."
with open("C:\\users\\ryanm\\desktop\\acct_id_email.csv", 'rb') as RE:
    reader_alt = csv.reader(RE, delimiter=',')

    header = reader_alt.next()

    for row in reader_alt:
        account_id = row[header.index("account")]
        email = row[header.index("email")]

        accounts[account_id] = email

print "Matching emails..."
with open('\\\\filer01\\public\\RobJ\\LAM\\sfidAcct.csv', 'rb') as R:
    reader = csv.reader(R, delimiter=',')

    with open("C:\\users\\ryanm\\desktop\\emails_found.csv", 'wb') as W:
        writer = csv.writer(W, lineterminator='\n')

        main_header = ['SFID', 'account_id', 'email']

        header = reader.next()

        account_values = accounts.values()

        for row in reader:
            acct_id = row[header.index('AccountID')]
            email = row[header.index("Email")]
            sfid = row[header.index('AccountSFId')]

            if email in account_values and email != "":
                final = sfid, acct_id, email
                writer.writerow(final)


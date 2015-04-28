import RequestService.splunk_requests as sr
import datetime
import csv


end = datetime.datetime(2015, 2, 1)
start = datetime.datetime(2014, 2, 1)
search = 'search sourcetype=PSPAudit EventName=Login NOT Email=*@payscale.com* NOT Email="NA" | join AccountID' \
         ' [search sourcetype=PSPAccount (SubscriptionType="PSPV2" OR SubscriptionType="PSPV2 AD-HOC") ' \
         'IsInternal=false NOT SalesForceID=NA | fields - Created ] |Table Created, AccountID, ' \
         'AccountName, SalesForceID, SubscriptionType, EventName, Email'

splunk_logs = sr.SplunkRequests(start, end)
splunk_logs.set_search_string(search)
results = splunk_logs.pull_psp_job_match_splunk_logs()

with open("C:\\users\\ryanm\\desktop\\TestData.csv", 'wb') as W:
    writer = csv.writer(W, lineterminator='\n')

    write_header = ['Created', 'AccountID', 'AccountName', 'SalesForceAccountID', 'SubscriptionType',
                    'EventName', 'Email']

    writer.writerow(write_header)

    is_first = True
    print "Waiting for results to populate... big time..."
    for dictionary in results:
        if is_first is True:
            print "Beginning to write results to file..."
            is_first = False
            continue
        row = []
        for item in dictionary:
            new_item = dictionary[item]
            row.append(new_item)
        writer.writerow(row)
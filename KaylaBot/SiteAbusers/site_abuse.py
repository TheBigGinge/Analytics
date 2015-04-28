import hmac
import hashlib
from datetime import datetime
import DateFunctions.datetimes_in as df
import SqlTools.payscale_replicated as pr
import datetime
import urllib
import json


"""Script to find all the main site abusers by IP"""
out_path = '\\\\filer01\\public\\Data_Analytics\\SiteAbusers\\'
data = pr.SqlServer("SiteStats")
ip_results = {}

dates = df.DateTimeFormats()

first_of_last = dates.return_ymd_first_of_last_month("-")
last_of_last = dates.return_ymd_last_day_of_last_month().strftime("%Y-%m-%d")
#Main SQl Query. Need to be authenticated to the firewall


query = '''
declare     @StartDate datetime
declare     @EndDate datetime
declare     @pageName varchar(255)
declare     @codeName varchar(255)
declare     @codeVal varchar(255)

set @StartDate = '{0}'

set @EndDate = '{1}'
set @pageName = '/mypayscale.aspx'
set @codeName = 'ProfileGuid'

-- logtoken token_types: VISITOR, IPADDR, CODENAME, CODEVAL, PAGENAME, USERAGNT, REFERER

-- get unique profiles viewed on my payscale

select lt.token_value as ip_address, count(distinct plf.code_value_id) as cnt
from ProcessedLogFiles plf with  (nolock)
inner join LogTokens lt on lt.token_id = plf.ip_address
where
      plf.date_created < @EndDate and plf.date_created > @StartDate and
      plf.PAGE_NAME_ID = (select token_id FROM LogTokens WHERE Token_type = 'PAGENAME' AND token_value_for_index = @pageName) and
      plf.code_name_id = (select token_id FROM LogTokens WHERE Token_type = 'CODENAME' AND token_value_for_index = @codeName)
group by lt.token_value order by cnt desc
'''.format(first_of_last, last_of_last)


print "Pulling ip addresses and counts from sql..."
data.set_query_string(query)

data.initialize_connection()

for row in data.return_results():
    print row.ip_address, row.cnt
    ip_results[row.ip_address] = row.cnt


print "Pulling ip signatures, records and writing to file..."
current_date = dates.return_year_month_as_string("-")
with open(out_path + current_date + " SiteAbusers.txt", 'wb') as W:

    for ip_address in ip_results:
        count = ip_results[ip_address]
        if int(count) >= 20:

            print 'Accessing IP Address: ' + ip_address

            if __name__ == "__main__":
                api_username = 'devKaylaH'
                api_key = '7d9af-6651a-f913b-2376e-2e466'
                host = 'freeapi.domaintools.com'

                new_url = 'http://{0}/v1/{1}/whois?api_username={2}&api_key={3}'.format(
                    host, ip_address, api_username, api_key)

                content = json.loads(urllib.urlopen(new_url).read())

                try:
                    registrant = content['response']['registrant']
                except KeyError:
                    registrant = 'N/A'

                try:
                    record = content['response']['whois']['record']
                except KeyError:
                    record = "N/A"

                header = "%s (%s) : %s" % (registrant, ip_address, count) + "\n"
                W.write(header)
                try:
                    record += "\n"
                    W.write(record)
                except UnicodeEncodeError:
                    W.write("Couldn't write information. You'll need to pull this by hand.")

print "%s is written to file" % (current_date + " SiteAbusers.txt")
import splunklib.client as client
import splunklib.results as results
import DateFunctions.date_functions as df


class SplunkRequests:

    def __init__(self, min_date, max_date):
        self.host = 'digger'
        self.user = 'jessew'
        self.password = 'Payscale'
        self.port = 8089
        self.date_format = df.DateFunctions()
        self.min_date = min_date
        self.max_date = max_date
        self.search_string = "search sourcetype=PSPJobMatching | table AccountID, AccountName, Algorithm, AllQueries," \
                             " Created, Email, JobIndex, NumSearches, NumViewMore, PayscaleTitle, Query, " \
                             "SalesForceAccountID, SubscriptionType"

    def pull_psp_job_match_splunk_logs(self):

        service = client.connect(host=self.host, port=self.port,
                                 username=self.user, password=self.password)

        kwargs_one_shot = {"earliest_time": self.date_format.splunk_date_format(self.min_date),
                           "latest_time": self.date_format.splunk_date_format(self.max_date),
                           "count": "500000"}

        print "Pulling splunk data..."

        one_shot_search_results = service.jobs.oneshot(self.search_string, **kwargs_one_shot)

        reader = results.ResultsReader(one_shot_search_results)

        print "Successful pull"

        return reader

    def set_search_string(self, new_string):
        self.search_string = new_string

SplunkRequests("2015-08-01", "2015-09-01").pull_psp_job_match_splunk_logs()
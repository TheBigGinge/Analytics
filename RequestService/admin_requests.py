import requests
import json
import os
import getpass
import base64


class PullAnyAffinityType:

    def __init__(self, body_search, name_search, properties, file_name, file_path=None):
        """
        Uses the RESTful webservice bulkdataservice to pull affinity information into a
        tsv file. Designed for the Data Dashboard but can have many uses for many programs
        where you want to programmtically have all the current affinties.
        Args:
            body_search: needs to be either a search string or a None value
            name_search: needs to be either a search string or a None value
            properties: a dictionary (string, string) with (property name: property value)
                        combinations.
            file_name: name of the output file
            file_path: string leading to a the output director. If not specified is written
                        to your desktop.
        Returns:
            A .tsv file of your affinity rules
        Example Call:
            PullAnyAffinityType(None, None, {'field': 'job', 'breadth': '10'}, "Current Job Rollups")

        """
        self.url = "http://psstats03:80/bulkdataservice.svc/affinities"
        self.body_search = body_search
        self.name_search = name_search
        self.properties = properties
        self.file_name = file_name
        self.file_location = file_path
        self.value_test()
        self.call_service_and_pull_data()

    def value_test(self):

        assert isinstance(self.properties, dict), "Property names aren't given in a dictionary"

        for value in self.properties:
            value.lower().strip()

        if self.body_search is not None:
            self.body_search.lower().strip()

        if self.name_search is not None:
            self.name_search.lower().strip()

    def place_values_into_json_string(self):

        json_build = {'ruleID': None, 'nameSearch': self.name_search, 'bodySearch': self.body_search,
                      'properties': self.properties}

        json_string = json.dumps(json_build)

        return json_string

    def call_service_and_pull_data(self):

        print "Pulling affinity data from the admin tool... \n"

        json_string = self.place_values_into_json_string()

        if self.file_location is None:
            file_location = os.path.expanduser("~"+getpass.getuser())+"\\desktop\\" + self.file_name + ".tsv"
        else:
            file_location = "\\\\filer01\\public\\Data Dashboards\\Automated Dashboard Files\\" + self.file_name \
                            + ".tsv"

        with open(file_location, 'wb') as writer:
            r = requests.post(self.url, data=json_string)

            if r.status_code == 200:
                print "Successful pull. Writing to file \n"
            else:
                print "Something went wrong with the affinity data pull. You'll need to try again. \n"
                print "Status code: " + str(r.status_code)

            for chunks in r.iter_content(1000):
                writer.write(chunks)


class PullCurrentAnswerValues:

    def __init__(self, answer_value, confirmed, out_dir=None):
        """
        Args:
            answer_value: string value representing a field
            confirmed: integer of 1 means unconfirmed while 2 means confirmed
            out_dir: string representing the directory where the file is written out to
        Returns:
            a .tsv file of the answervalues
        Example:
            PullCurrentAnswerValues("job", 2)
        """
        self.url = "http://psstats03:80/bulkdataservice.svc/answervalues/"
        self.out_dir = out_dir
        self.answer_value = answer_value
        self.confirmed = confirmed
        self.value_test()
        self.run()

    def value_test(self):
        assert isinstance(self.answer_value, str), "Answervalue must be a string"
        assert isinstance(self.confirmed, int), "The confirmed flag must be an integer"

        if self.confirmed not in [1, 2]:
            print "The confirmed flag must be an integer of either 1 for unconfirmed or 2 for confirmed"
            raise SystemExit
        else:
            self.confirmed = str(self.confirmed)
            self.url += self.answer_value + "/" + self.confirmed

    def run(self):
        if self.out_dir is None:
            file_location = os.path.expanduser("~"+getpass.getuser())+"\\desktop\\AnswerValues.tsv"
        else:
            file_location = self.out_dir

        print "Pulling Current AnswerValues from the admin tool"

        with open(file_location, 'wb') as writer:
            r = requests.get(self.url)

            if r.status_code == 200:
                print "Successful pull. Writing to file \n"
            else:
                print "Something went wrong with the answervalue data pull. You'll need to try again. \n"
                print "Status code: " + str(r.status_code)

            for chunks in r.iter_content(1000):
                writer.write(chunks)


class PullTaskSeedProfiles:

    def __init__(self, out_file):
        """
        Pulls all of the current tasks into a .tsv file.

        :param out_file:
            Location and file name where you want the data sent to
        :return:
            A .tsv file of all the current tasks.
        """
        self.url = "http://psstats03:80/bulkdataservice.svc/taskseedprofiles"
        self.out_file = out_file

    def run(self):

        with open(self.out_file, 'wb') as writer:
            print "Sending request..."
            r = requests.get(self.url)

            if r.status_code == 200:
                print "Successful pull. Writing to file \n"
            else:
                print "Something went wrong with the answervalue data pull. You'll need to try again. \n"
                print "Status code: " + str(r.status_code)

            for chunks in r.iter_content(1000):
                writer.write(chunks)


class PostToAnalysisTool:

    def __init__(self, file_location, out_file, ui_update=None):
        """
        This is designed to give you a programmatic way to run analysis tool queries against
        psstats03. If you are going to bulk run queries please do so during off working hours
        so we don't hold up any of the analysts.

        Best used in conjunction with the serialize_xml.py script so you don't have to hand build your
        xml to send to the analysis tool.

        :param file_location:
            Location of the .txt file that holds the Analysis.config xml.
        :param out_file:
            Location and file name that you want the results exported to. The results are zipped.
        :return:
            A .zip file containing a .xml file for all of the file dimensions ran in the query.
        """
        self.url = "http://psstats03:80/analysistoolservice.svc/report/anon"
        self.file_location = file_location
        self.out_file = out_file
        self.ui_update = ui_update

    def run(self):

        report_name = self.file_location[self.file_location.rfind("\\") + 1:]
        print "POSTing " + report_name + "..."

        with open(self.file_location, 'rb') as reader:
            with open(self.out_file, 'wb') as writer:
                r = requests.post(self.url, data=reader)

                if r.status_code == 200:

                    print "Successful pull. Writing to file"

                    if self.ui_update is not None:
                        self.ui_update.emit('Successful pull. Writing to file...')

                else:
                    print "Something went wrong with the Analysis Tool Post request. You'll need to try again. \n"
                    print "Status code: " + str(r.status_code)

                for chunks in r.iter_content(1000):
                    writer.write(chunks)
                print "Results writing completed."

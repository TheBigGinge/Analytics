import json


class RawTaskLogSupport:

    def __init__(self, survey_dict):
        self.dates = []
        self.profile_dictionary = {}
        self.survey_dict = survey_dict

    def open_raw_task_file(self, target_file, directory):

        lines_read = 0
        line_breaks = 0
        missing_guid = 0
        with open(directory + target_file, 'rb') as R:
            target_line = R.readline()

            while target_line:
                lines_read += 1
                if lines_read % 10000 == 0:
                    print "%s lines read..." % lines_read
                try:
                    output = json.loads(target_line)
                    self.classify_data(output, lines_read, missing_guid)
                except UnicodeDecodeError:
                    line_breaks += 1

                target_line = R.readline()

        print "%s line breaks" % line_breaks
        print "%s missing guids"

    def classify_data(self, output, lines_read, missing_guid):
        entry_date = output['EntryTime'].encode('ascii', 'replace')
        guid = output['ProfileId'].encode('ascii', 'replace')
        job_title = output['JobTitle'].encode('ascii', 'replace')

        try:
            survey_type = self.survey_dict[guid]
        except KeyError:
            survey_type = 'Unknown'
            missing_guid += 1
        tasks = None
        visible = None
        do_not_apply = None
        task_test = None
        try:
            output['Visible']
            visible = 1
        except KeyError:
            visible = 0

        try:
            task_test = output['SelectedJobTasks']
            tasks = 1
            visible = 1
        except KeyError:
            tasks = 0

        if tasks == 1 and len(task_test) > 0:
            if task_test[0] == 'None of these tasks apply to me':
                do_not_apply = 1
            else:
                do_not_apply = 0

        if task_test is not None and len(task_test) == 0:
            print lines_read

        self.dates.append(entry_date)
        final_set = entry_date, job_title, visible, do_not_apply, tasks, survey_type
        self.profile_dictionary[guid] = final_set

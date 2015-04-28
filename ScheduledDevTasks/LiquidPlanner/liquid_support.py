from RequestService import liquid_requests as lr


class LiquidSupport:

    project_id = 16976447

    def __init__(self, project_id=None):
        if project_id is not None:
            self.project_id = project_id

        self.lpr = self.setup_liquid()
        self.project_task_dictionaries = self.project_tasks()

    def setup_liquid(self):

        lpr = lr.LiquidPlannerRequest()
        workspace = lpr.workspaces()[0]
        lpr.set_workspace_id(workspace['id'])
        lpr.set_project_id(str(self.project_id))

        return lpr

    def task_locations(self):
        task_location = {}
        all_tasks = self.lpr.pull_all_tasks()

        for task in all_tasks:
            task_location[task['id']] = task['parent_id']

        return task_location

    def project_tasks(self):
        project_tasks = []
        all_tasks = self.lpr.pull_all_tasks()

        for task in all_tasks:

            if str(task['parent_id']) == str(self.project_id):
                project_tasks.append(task)

        return project_tasks

    def extract_email_from_note(self, task_id):

        note = self.lpr.pull_task_note(task_id)
        return self.note_html_parse(note)

    @staticmethod
    def note_html_parse(note):

        parse_start = note[note.find("mailto:") + len("mailto:"):]
        email = parse_start[:parse_start.find('">')].strip()
        return email

    def pull_task_dictionary(self, task_id):
        return self.lpr.pull_task_by_id(task_id)

    def current_active_tasks(self):
        active_tasks = []

        for task in self.project_task_dictionaries:
            if str(task['is_done']) is 'False':
                active_tasks.append(task)

        return active_tasks

    @staticmethod
    def check_for_task_changes(stored_task, liquid_task):
        stored_date = stored_task['updated_at']
        liquid_date = liquid_task['updated_at']

        stored_is_done = stored_task['is_done']
        liquid_is_done = liquid_task['is_done']

        stored_earliest_start = stored_task['earliest_start']
        liquid_earliest_start = liquid_task['earliest_start']

        stored_expected_start = stored_task['expected_start']
        liquid_expected_start = liquid_task['expected_start']

        stored_earliest_finish = stored_task['earliest_finish']
        liquid_earliest_finish = liquid_task['earliest_finish']

        stored_expected_finish = stored_task['expected_finish']
        liquid_expected_finish = liquid_task['expected_finish']

        check_list = [(stored_date, liquid_date), (stored_is_done, liquid_is_done),
                      (stored_earliest_start, liquid_earliest_start), (stored_expected_start, liquid_expected_start),
                      (stored_earliest_finish, liquid_earliest_finish),
                      (stored_expected_finish, liquid_expected_finish)]

        difference = False

        for items in check_list:
            if str(items[0]) != str(items[1]):
                difference = True

        if str(stored_is_done) == "True" and str(liquid_is_done) == "True":
            difference = False

        return difference

    def pull_all_changes(self):
        return self.lpr.check_for_task_changes()
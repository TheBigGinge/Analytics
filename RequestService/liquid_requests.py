import requests
import json
import os
import getpass
import base64


class LiquidPlannerRequest:

    base_uri = 'https://app.liquidplanner.com/api'
    workspace_id = None
    project_id = None
    email = 'ryanm@payscale.com'
    password = 'Huge-Large1978'
    session = None

    def __init__(self, email=None, password=None):
        if email is not None:
            self.email = email
            self.password = password

    def get_workspace_id(self):
        return self.workspace_id

    def set_workspace_id(self, workspace_id):
        self.workspace_id = workspace_id

    def set_project_id(self, project_id):
        self.project_id = project_id

    def get(self, uri, options={}):
        return requests.get(self.base_uri + uri,
                            data=options,
                            headers={'Content-Type': 'application/json'},
                            auth=(self.email, self.password))

    def post(self, uri, options={}):
        return requests.post(self.base_uri + uri,
                             data=options,
                             headers={'Content-Type': 'application/json'},
                             auth=(self.email, self.password))

    def put(self, uri, options={}):
        return requests.put(self.base_uri + uri,
                            data=options,
                            headers={'Content-Type': 'application/json'},
                            auth=(self.email, self.password))

    def account(self):
        """
        Returns a dictionary with information about the current user.
        """
        return json.loads(self.get('/account').content)

    def workspaces(self):
        """
        Returns a list of dictionaries, each a workspace in which the user is a member
        Workspaces are the root directory
        """
        return json.loads(self.get('/workspaces').content)

    def packages(self):
        """
        Returns a dictionary of all packages
        A workspace is made up of packages
        """
        return json.loads(self.get('/workspaces/' + str(self.workspace_id) +
                          '/packages').content)

    def projects(self):
        """
        Returns a list of dictionaries, each a project in a workspace
        A package can be made up of projects and tasks
        """
        return json.loads(self.get('/workspaces/' + str(self.workspace_id) +
                          '/projects').content)

    def pull_all_tasks(self):
        """
        Returns a list of dictionaries, each a task in a workspace
        Tasks can live in projects or packages
        """
        return json.loads(self.get('/workspaces/' + str(self.workspace_id) +
                          '/tasks').content)

    def create_task(self, data):
        """
        Creates a task by POSTing data
        :params data:
            Commands for the api
        """
        return json.loads(self.post('/workspaces/' + str(self.workspace_id) +
                          '/tasks', json.dumps({'task': data})).content)

    def update_task(self, data):
        """
        Updates a task by PUTing data
        :params data:
            Commands for the api
        """
        return json.loads(self.put('/workspaces/' + str(self.workspace_id) +
                          '/tasks/' + str(data['id']), json.dumps({'task': data})).content)

    def write_task_comment(self, task_id, comment):
        """
        Writes a comment to a task
        """
        return json.loads(self.post('/workspaces/' + str(self.workspace_id) +
                          '/tasks/' + str(task_id) + '/comments', json.dumps({'comment': comment})).content)

    def check_for_task_changes(self):
        return json.loads(self.get('/workspaces/' + str(self.workspace_id)
                          + '/changes').content)

    def pull_task_by_id(self, id_number):
        """
        Returns a list of dictionaries, each a task in a workspace
        Tasks can live in projects or packages
        """
        return json.loads(self.get('/workspaces/' + str(self.workspace_id) +
                          '/tasks/' + str(id_number)).content)

    def pull_task_note(self, task_id):

        return self.get('/workspaces/' + str(self.workspace_id) +
                        '/tasks/' + str(task_id) + '/note').content
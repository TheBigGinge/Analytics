import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class LiquidEmail:

    def __init__(self, task_dict, liquid_dict=None):
        self.task_dict = task_dict
        self.liquid_dict = liquid_dict
        self.main_email = "Liquid Alerts@payscale.com"
        self.msg = MIMEMultipart()
        self.msg['Subject'] = "Desktop Support Update"
        self.intro = "Your Desktop Support case has been updated: "
        self.email_out = None
        self.set_email_out()
        self.header = None
        self.earliest_start = None
        self.expected_start = None
        self.earliest_finish = None
        self.expected_finish = None
        self.is_done = None
        self.server = smtplib.SMTP('owa.payscale.com')

    def set_email_out(self):
        self.email_out = [self.task_dict['email_origin']]

    def pull_task_information(self):
        if self.liquid_dict is None:
            self.header = self.task_dict['name']
            self.earliest_start = self.task_dict['earliest_start']
            self.expected_start = self.task_dict['expected_start']
            self.earliest_finish = self.task_dict['earliest_finish']
            self.expected_finish = self.task_dict['expected_finish']
            self.is_done = str(self.task_dict['is_done'])
        else:
            self.header = self.task_dict['name']
            self.earliest_start = self.liquid_dict['earliest_start']
            self.expected_start = self.liquid_dict['expected_start']
            self.earliest_finish = self.liquid_dict['earliest_finish']
            self.expected_finish = self.liquid_dict['expected_finish']
            self.is_done = str(self.liquid_dict['is_done'])

    def create_updated_message(self):
        if str(self.is_done).lower() is "true":
            completed = "Your case has been completed"
        else:
            completed = "Your case is still ongoing"

        first_message = "Earliest Start: " + self.earliest_start[:self.earliest_start.find("+")].replace("T", " ")
        second_message = "Expected Start: " + self.expected_start[:self.expected_start.find("+")].replace("T", " ")
        third_message = "Earliest Finish: " + self.earliest_finish[:self.earliest_finish.find("+")].replace("T", " ")
        fourth_message = "Expected Finish: " + self.expected_finish[:self.expected_finish.find("+")].replace("T", " ")
        fifth_message = "Task Complete: " + completed

        msg_text = MIMEText('<br></br>%s<br></br>%s<br></br>%s<br></br>%s<br></br>%s<br></br>'
                            '%s<br>%s<br>' %
                           (self.intro, self.header, first_message, second_message, third_message, fourth_message,
                            fifth_message), 'html')

        self.msg.attach(msg_text)

    def send_updated_message(self):
        self.pull_task_information()
        self.create_updated_message()
        self.server.sendmail(self.main_email, self.email_out, self.msg.as_string())
        self.server.quit()

    def newly_created_message(self):
        msg_text = MIMEText("Your case '" + str(self.header) + "' has been filed. You will be notified when "
                            "this case has been prioritized and completed. \n -Desktop Support")
        self.msg.attach(msg_text)

    def send_new_task_message(self):
        self.pull_task_information()
        self.newly_created_message()
        self.server.sendmail(self.main_email, self.email_out, self.msg.as_string())
        self.server.quit()
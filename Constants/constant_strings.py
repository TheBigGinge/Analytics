import os
import getpass

class Constants:
    def __init__(self):
        """Analytics Folder"""
        self.data_analytics = '\\\\filer02\\public\\Data_Analytics\\'
        self.aequitas = self.data_analytics + 'Aequitas\\'
        self.anon_reports = self.data_analytics + 'AnonReports\\'
        self.anon_in = self.anon_reports + 'TempIn\\'
        self.alumni_analytics_in = self.anon_in + '\\GinaDimensions\\'
        self.anon_out = self.anon_reports + 'TempOut\\'
        self.consumer_level_conversion = self.data_analytics + 'Consumer_Level_Conversion\\'
        self.consumer_alert_files = self.consumer_level_conversion + 'Alert_Files\\'
        self.question_dashboard = self.data_analytics + 'Answer Conversion Activation and Bail Rates\\'
        self.profile_counts = self.data_analytics + 'ProfileCountsByType\\'

        self.consumer_log_metrics = '\\\\filer01\\public\\Data_Analytics\\Consumer Log Metrics\\'
        self.consumer_log_data = self.consumer_log_metrics + 'Data Files\\'


        self.log_path = '\\\\psfiler01\\data\\SurveyReports\\'

        """Local path directories"""
        self.local_path = os.path.expanduser("~" + getpass.getuser())
        self.local_desktop =  self.local_path +  "\\desktop\\"
        self.local_documents = self.local_path + '\\Documents\\'
        self.git_hub = self.local_documents + '\\GitHub\\'
        self.git_hub_analytics = self.git_hub + '\\Analytics\\'
        self.payscale_analytics = self.git_hub_analytics + '\\PayScaleAnalytics\\'

        """Data Dashboard"""
        self.data_dashboard = '\\\\filer02\\public\\Data Dashboards\\'
        self.automated_dashboard_files = self.data_dashboard + 'Automated Dashboard Files\\'
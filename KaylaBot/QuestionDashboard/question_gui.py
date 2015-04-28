import os
import getpass
import csv

from PyQt4 import QtCore, QtGui

from KaylaBot.QuestionDashboard import question_database as db
import gui_code_behind as support
import data_extract_thread as analysis
import gui_code_behind as cb


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class UiMainWindow(object):

    def __init__(self):
        self.central_widget = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = None
        self.text_edit = None
        self.start_date = None
        self.analysis_tool_button = None
        self.label = None
        self.label_2 = None
        self.progressBar = None
        self.csv_button = None
        self.label_3 = None
        self.breadth_30 = None
        self.breadth_40 = None
        self.breadth_50 = None
        self.breadth_60 = None
        self.overall_breadth = None
        self.status_bar = None
        self.log_thread = None
        self.data_pull_thread = None
        self.pull_csv_thread = None
        self.check_boxes = None
        self.csv_thread = None
        self.local_path = os.path.expanduser("~" + getpass.getuser()) + "\\desktop\\"
        self.support = support.QuestionDashSupport()

    def setup_ui(self, main_window):
        main_window.setObjectName(_fromUtf8("MainWindow"))
        main_window.resize(800, 600)
        main_window.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Question Dashboard", None,
                                                                QtGui.QApplication.UnicodeUTF8))
        self.central_widget = QtGui.QWidget(main_window)
        self.central_widget.setObjectName(_fromUtf8("central_widget"))
        self.scrollArea = QtGui.QScrollArea(self.central_widget)
        self.scrollArea.setGeometry(QtCore.QRect(120, 240, 541, 271))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 539, 269))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.text_edit = QtGui.QTextEdit(self.scrollAreaWidgetContents)
        self.text_edit.setGeometry(QtCore.QRect(0, 0, 541, 271))
        self.text_edit.setObjectName(_fromUtf8("textEdit"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.start_date = QtGui.QDateEdit(self.central_widget)
        self.start_date.setGeometry(QtCore.QRect(120, 110, 110, 22))
        self.start_date.setDate(QtCore.QDate(2014, 7, 1))
        self.start_date.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2014, 7, 1), QtCore.QTime(0, 0, 0)))
        self.start_date.setObjectName(_fromUtf8("start_date"))

        self.analysis_tool_button = QtGui.QPushButton(self.central_widget)
        self.analysis_tool_button.setGeometry(QtCore.QRect(120, 520, 131, 28))
        self.analysis_tool_button.setText(QtGui.QApplication.translate("MainWindow", "Update Data", None,
                                                                       QtGui.QApplication.UnicodeUTF8))
        self.analysis_tool_button.setObjectName(_fromUtf8("pushButton"))
        self.analysis_tool_button.setToolTip('This will update data from the given date range from the Analysis Tool'
                                             ' and the log files. Do not run until the beginning of the month '
                                             'when running the previous month.')
        self.label = QtGui.QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(120, 80, 71, 16))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Start Date", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))

        self.progressBar = QtGui.QProgressBar(self.central_widget)
        self.progressBar.setGeometry(QtCore.QRect(280, 520, 281, 31))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.csv_button = QtGui.QPushButton(self.central_widget)
        self.csv_button.setGeometry(QtCore.QRect(420, 180, 111, 41))
        self.csv_button.setText(QtGui.QApplication.translate("MainWindow", "Pull Data To CSV", None,
                                                             QtGui.QApplication.UnicodeUTF8))
        self.csv_button.setObjectName(_fromUtf8("pushButton_2"))
        self.csv_button.setToolTip('This will pull data from the given date range into a csv file to your desktop for '
                                   'the given Breadths.')
        self.label_3 = QtGui.QLabel(self.central_widget)
        self.label_3.setGeometry(QtCore.QRect(570, 530, 101, 16))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Query Progress", None,
                                                          QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.breadth_30 = QtGui.QCheckBox(self.central_widget)
        self.breadth_30.setGeometry(QtCore.QRect(420, 100, 91, 20))
        self.breadth_30.setText(QtGui.QApplication.translate("MainWindow", "Breadth 30", None,
                                                           QtGui.QApplication.UnicodeUTF8))
        self.breadth_30.setObjectName(_fromUtf8("breadth_30"))
        self.breadth_40 = QtGui.QCheckBox(self.central_widget)
        self.breadth_40.setGeometry(QtCore.QRect(420, 140, 91, 20))
        self.breadth_40.setText(QtGui.QApplication.translate("MainWindow", "Breadth 40", None,
                                                             QtGui.QApplication.UnicodeUTF8))
        self.breadth_40.setObjectName(_fromUtf8("breadth_40"))
        self.breadth_50 = QtGui.QCheckBox(self.central_widget)
        self.breadth_50.setGeometry(QtCore.QRect(540, 140, 91, 20))
        self.breadth_50.setText(QtGui.QApplication.translate("MainWindow", "Breadth 50", None,
                                                             QtGui.QApplication.UnicodeUTF8))
        self.breadth_50.setObjectName(_fromUtf8("breadth_50"))
        self.breadth_60 = QtGui.QCheckBox(self.central_widget)
        self.breadth_60.setGeometry(QtCore.QRect(540, 100, 91, 20))
        self.breadth_60.setText(QtGui.QApplication.translate("MainWindow", "Breadth 60", None,
                                                             QtGui.QApplication.UnicodeUTF8))
        self.breadth_60.setObjectName(_fromUtf8("breadth_60"))
        self.overall_breadth = QtGui.QCheckBox(self.central_widget)
        self.overall_breadth.setGeometry(QtCore.QRect(540, 190, 91, 20))
        self.overall_breadth.setText(QtGui.QApplication.translate("MainWindow", "Overall", None,
                                                                  QtGui.QApplication.UnicodeUTF8))

        self.data_pull_thread = analysis.ExtractDataThread()
        self.data_pull_thread.update_string_progress.connect(self.set_string_progress)
        self.data_pull_thread.update_progress.connect(self.set_progress)

        self.overall_breadth.setObjectName(_fromUtf8("overall_breadths"))
        main_window.setCentralWidget(self.central_widget)
        self.status_bar = QtGui.QStatusBar(main_window)
        self.status_bar.setObjectName(_fromUtf8("status_bar"))
        main_window.setStatusBar(self.status_bar)

        self.progressBar.setRange(0, self.support.count_number_of_files_to_process(self.start_date))

        self.re_translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def re_translate_ui(self, main_window):
        self.progressBar.setValue(0)
        self.analysis_tool_button.clicked.connect(self.pull_current_data)
        self.csv_button.clicked.connect(self.pull_data_to_csv)

    def set_progress(self, progress):
        self.progressBar.setValue(progress)

    def set_string_progress(self, progress):
        self.text_edit.append(progress)

    def pull_current_data(self):
        if not self.data_pull_thread.isRunning():
            self.data_pull_thread.get_date(self.start_date)
            self.data_pull_thread.start()

    def pull_data_to_csv(self):
        if self.no_check_boxes_check():
            self.check_boxes = [self.breadth_30.isChecked(), self.breadth_40.isChecked(), self.breadth_50.isChecked(),
                                self.breadth_60.isChecked(), self.overall_breadth.isChecked()]
            #Couldn't get the csv thread to interact with gui tool so I moved the code to here
            #TODO: Get the csv thread to work and move this code out of here
            if int(self.start_date.date().toPyDate().strftime("%Y%m")) in db.QuestionDashboardData().get_all_dates():
                self.write_data_to_file()
            else:
                self.text_edit.append("The month / year you chose isn't in the database yet.")

    def no_check_boxes_check(self):

        if not self.breadth_30.isChecked() and not self.breadth_40.isChecked() and not self.breadth_50.isChecked()\
                and not self.breadth_60.isChecked() and not self.overall_breadth.isChecked():
                    self.text_edit.append("You need to choose at least one breadth first \n")
                    return False
        else:
            return True

    def write_data_to_file(self):

        file_name = "Question_Dashboard"
        if self.count_files() != 0:
            number = self.count_files()
            file_name = file_name + "(" + str(number) + ").csv"
        else:
            file_name += ".csv"

        update_line = "Writing to file at %s" % self.local_path + file_name
        self.text_edit.append(update_line)
        with open(self.local_path + file_name, 'wb') as W:
            writer = csv.writer(W, lineterminator='\n')

            if self.check_boxes[0] is True:
                self.write_breadth_to_file(writer, 'thirty')
            if self.check_boxes[1] is True:
                self.write_breadth_to_file(writer, 'forty')
            if self.check_boxes[2] is True:
                self.write_breadth_to_file(writer, 'fifty')
            if self.check_boxes[3] is True:
                self.write_breadth_to_file(writer, 'sixty')
            if self.check_boxes[4] is True:
                self.write_overall_to_file(writer)

        self.text_edit.append("File writing complete.")

    def write_overall_to_file(self, writer):

        header = ['Date', 'Question', 'Overall', 'Active Profiles', 'Bailed 20', 'Saw 20', 'Saw MyPayScale',
                  'Total Counts']
        writer.writerow(header)

        for question in cb.QuestionDashSupport().get_all_the_questions():

            data = db.QuestionDashboardData().pull_all_non_breadth_data(question, self.start_date)

            for row in data:
                final = row[0], question, row[1], row[2], row[3], row[4], row[5], row[6]
                if row[1] != "":
                    writer.writerow(final)

    def write_breadth_to_file(self, writer, breadth):

        header = ['Date', 'Question', breadth, 'Active Profiles', 'Bailed 20', 'Saw 20', 'Saw MyPayScale',
                  'Total Counts']
        writer.writerow(header)

        for question in cb.QuestionDashSupport().get_all_the_questions():

            data = db.QuestionDashboardData().pull_breadth_x_data(question,
                                                                  self.start_date.date().toPyDate().strftime("%Y%m"),
                                                                  breadth)

            for row in data:
                final = row[0], question, row[1], row[2], row[3], row[4], row[5], row[6]
                if row[1] != "":
                    writer.writerow(final)

    def count_files(self):

        possible_dupes = os.listdir(self.local_path)
        dupes = 0

        for files in possible_dupes:
            if 'Question_Dashboard' in files:
                dupes += 1

        return dupes


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


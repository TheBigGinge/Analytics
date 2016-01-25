import get_alumni_data as gad

#---------------------#
#All report Definitions
#---------------------#

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def __int__(self):
        self.start_date = None
        self.end_date = None
        self.affiliate_id = None
        self.query_base_name = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(524, 230)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Alumni Analytics",
                                                               None, QtGui.QApplication.UnicodeUTF8))

        self.query_base_name = 'Gina Alumni Analytics Query '

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.start_date = QtGui.QDateEdit(self.centralwidget)
        self.start_date.setGeometry(QtCore.QRect(20, 50, 131, 22))
        self.start_date.setObjectName(_fromUtf8("dateTimeEdit"))
        self.start_date.setDate(QtCore.QDate(2015, 12, 1))
        self.end_date = QtGui.QDateEdit(self.centralwidget)
        self.end_date.setGeometry(QtCore.QRect(180, 50, 131, 22))
        self.end_date.setObjectName(_fromUtf8("dateTimeEdit_2"))
        self.end_date.setDate(QtCore.QDate(2015, 12, 2))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 131, 16))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Min Date",
                                                        None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 30, 131, 16))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Max Date",
                                                          None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 110, 381, 81))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(350, 30, 141, 16))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Affiliate ID: ",
                                                          None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.get_data_button = QtGui.QPushButton(self.centralwidget)
        self.get_data_button.setGeometry(QtCore.QRect(430, 160, 75, 23))
        self.get_data_button.setText(QtGui.QApplication.translate("MainWindow", "RUN IT!!!",
                                                             None, QtGui.QApplication.UnicodeUTF8))
        self.get_data_button.setObjectName(_fromUtf8("pushButton"))
        self.get_data_button.setToolTip('Fire off All The Analysis Tool Queries! for the given parameters')

        self.affiliate_id = QtGui.QLineEdit(self.centralwidget)
        self.affiliate_id.setGeometry(QtCore.QRect(350, 50, 141, 21))
        self.affiliate_id.setObjectName(_fromUtf8("lineEdit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 524, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.data_pull_thread = gad.AlumniDataCollect()
        self.data_pull_thread.update_string_progress.connect(self.set_string_progress)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.get_data_button.clicked.connect(self.pull_current_data)

    def pull_current_data(self):
        if not self.data_pull_thread.isRunning():
            self.data_pull_thread.get_date(self.start_date)
            self.data_pull_thread.get_date(self.end_date, False)
            self.data_pull_thread.set_main_filter(str(self.affiliate_id.text()))
            self.data_pull_thread.set_base_name(self.query_base_name)
            self.data_pull_thread.start()

    def set_string_progress(self, progress):
        self.textEdit.append(progress)



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
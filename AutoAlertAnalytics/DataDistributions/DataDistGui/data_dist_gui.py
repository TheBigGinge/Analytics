import sip
sip.setapi('QString', 1)
import gui_classes
import sys
import DateFunctions.date_functions as df
import pull_stats
from PyQt4 import QtGui
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

_encoding = QtGui.QApplication.UnicodeUTF8

data_headers = ("Active Profiles, Weekly", "All Profiles, Weekly", "EAC, Weekly",
                "Combined Salary, Weekly", "Company Sizes, Monthly", "Degree Level, Monthly",
                "NAICS 40, Monthly", "Age Distributions, Monthly", "ONET 40, Monthly",
                "YE, Monthly", "Rollups, Monthly", "Rollup & Metro, Monthly", "Metros, Monthly")


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.dates = gui_classes.Dates()
        self.variables = gui_classes.OtherVars()
        self.combo = None
        self.answer = None
        self.data = None
        self.init_ui()
        
    def init_ui(self):

        #Create main comboBox w/ Dist Types
        self.combo = QtGui.QComboBox()
        self.combo.addItems(data_headers)
        self.combo.setGeometry(QtCore.QRect(561, 41, 40, 40))
        self.combo.setAutoFillBackground(True)
        self.combo.setStyleSheet(_fromUtf8("background-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255,"
                                           " 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, "
                                           "255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, "
                                           "244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, "
                                           "255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, "
                                           "255, 0, 69), stop:1 rgba(255, 255, 0, 69));"))
        self.combo.setObjectName(_fromUtf8("comboBox"))

        self.combo.currentIndexChanged.connect(self.combo_changed)
        h_box_combo = QtGui.QHBoxLayout()
        h_box_combo.addWidget(self.combo)

        '''main (overall) layout'''
        v_box_main = QtGui.QVBoxLayout()
        v_box_main.addLayout(h_box_combo)
        v_box_main.addStretch(1)
        v_box_main.addLayout(self.dates.dateLayout)
        v_box_main.addStretch(1)
        v_box_main.addLayout(self.variables.variable_layout)
        v_box_main.addStretch(1)
        v_box_main.addLayout(self.variables.metro_layout)
        v_box_main.addStretch(8)

        '''Create Distribution Button'''
        end_button = QtGui.QPushButton("Show Data")
        end_button.clicked.connect(self.solver_alt)
        end_button.setGeometry(QtCore.QRect(390, 400, 201, 51))
        end_button.setAutoFillBackground(True)
        end_button.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 255);\n"
                                           "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,"
                                           " stop:0 rgba(9, 41, 4, 255), stop:0.085 rgba(2, "
                                           "79, 0, 255), stop:0.19 rgba(50, 147, 22, 255), stop:0.275 rgba(236, 191, "
                                           "49, 255), stop:0.39 rgba(243, 61, 34, 255),"
                                           " stop:0.555 rgba(135, 81, 60, 255), stop:0.667 rgba(121, 75, 255, 255), "
                                           "stop:0.825 rgba(164, 255, 244, 255), "
                                           "stop:0.885 rgba(104, 222, 71, 255), stop:1 rgba(93, 128, 0, 255));"))

        end_button.setObjectName(_fromUtf8("end_button"))

        end_button_2 = QtGui.QPushButton("Update Data")
        end_button_2.setGeometry(QtCore.QRect(50, 400, 201, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        end_button_2.setFont(font)
        end_button_2.setAutoFillBackground(False)
        end_button_2.setStyleSheet(_fromUtf8("background-color: qradialgradient(spread:repeat, cx:0.5, cy:0.5, "
                                             "radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(0, 169, 255, 147), "
                                             "stop:0.497326 rgba(0, 0, 0, 147), stop:1 rgba(0, 169, 255, 147));\n"
                                             "color: rgb(255, 0, 0);"))
        end_button_2.setObjectName(_fromUtf8("end_button_2"))
        #end_button_2.clicked.connect(update.UpdateDatabase)

        v_box_main.addWidget(end_button)
        v_box_main.addWidget(end_button_2)

        self.setLayout(v_box_main)
        self.setWindowTitle('Data Distribution Interface')
        self.setGeometry(300, 150, 639, 500)
        self.show()

    def solver_alt(self):
        self.answer = gui_classes.AnswerPopup()
        begin = df.DateFunctions().end_week(self.dates.startDate.date().toPyDate())
        end = df.DateFunctions().end_week(self.dates.endDate.date().toPyDate())

        self.data = pull_stats.Solver(self.combo.currentIndex(), begin, end,
                                      self.variables.variable_box.currentText(),
                                      self.variables.metroCountry.currentText(),
                                      self.variables.metroSt.currentText(),
                                      self.variables.metroCity.currentText())

        self.data.dist.canvas.setParent(self.answer)
        self.answer.setLayout(self.data.v_box_data)
        self.answer.show()

    def combo_changed(self):

        source = self.sender()
        source = str(source.currentText())

        '''check/change dates'''
        if "Weekly" in source:
            self.dates.switchDates(True)
        elif "Monthly" in source:
            self.dates.switchDates(False)

        '''check/change otherVars'''
        if source in data_headers[4:-1]:
            self.variables.set_other_variables(source)
        else:
            self.variables.remove_other_variable()

        '''check/change Metros'''
        if source in data_headers[-2:]:
            self.variables.areMetros(True)
        else:
            self.variables.areMetros(False)


def main():

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
import sqlite3

from PyQt4 import QtCore
from PyQt4 import QtGui

import DateFunctions.date_functions as df


class OtherVars(QtGui.QWidget):

    def __init__(self):
        super(OtherVars, self).__init__()
        self.file_path = "\\\\filer01\\public\\Data Analytics\\Data Distributions\\"
        self.is_variable = False
        self.is_metro = False
        self.variable_label = None
        self.variable_box = None
        self.box_filler = None
        self.variable_layout = QtGui.QVBoxLayout()
        self.metro_layout = QtGui.QVBoxLayout()
        #self.init_metros()
        self.init_other_variables()

    def init_other_variables(self):
        self.variable_label = QtGui.QLabel()
        self.variable_label.hide()
        self.variable_box = QtGui.QComboBox()
        self.variable_box.hide()

        '''layout'''
        self.variable_layout.addWidget(self.variable_label)
        self.variable_layout.addWidget(self.variable_box)

    def variable_names(self, variable):
        items = []

        '''These create the drop down text for the scroll bar'''
        conn = sqlite3.connect(self.file_path + "Database\\distributions.db")
        c = conn.cursor()

        if variable == "Company Sizes, Monthly":
            self.variable_label.setText("Size Range")
            for row in c.execute("SELECT DISTINCT size_range FROM company_size"):
                items.append(row[0])
        elif variable == "Degree Level, Monthly":
            self.variable_label.setText("Level of Education")
            for row in c.execute("SELECT DISTINCT level FROM degree_affinities"):
                items.append(row[0])
        elif variable == "NAICS 40, Monthly":
            self.variable_label.setText("NAICS Code")
            for row in c.execute("SELECT * FROM naics_names"):
                items.append(str(row[0]) + " - " + str(row[1]))
        elif variable == "Age Distributions, Monthly":
            self.variable_label.setText("Age Range")
            for row in c.execute("SELECT DISTINCT age_range FROM age_ranges"):
                items.append(row[0])
        elif variable == "ONET 40, Monthly":
            self.variable_label.setText("ONET 40 Name")
            for row in c.execute("SELECT * FROM onet_name"):
                items.append(str(row[0])+" - " + str(row[1]))
        elif variable == "YE, Monthly":
            self.variable_label.setText("Experience Range")
            for row in c.execute("SELECT DISTINCT experience_range FROM years_experience"):
                items.append(row[0])
        elif variable == "Rollups, Monthly" or variable == "Rollup & Metro, Monthly":
            self.variable_label.setText("Rollup Name")
            for row in c.execute("SELECT DISTINCT name FROM rollups"):
                items.append(row[0])

        items.sort()
        self.variable_box.addItems(items)
        conn.close()
        
    def set_other_variables(self, var):
        if self.is_variable is True:
            self.remove_other_variable()
        self.variable_names(var)
        self.variable_label.show()
        self.variable_box.show()
        self.is_variable = True
        
    def remove_other_variable(self):
        if self.is_variable is False:
            return
        else:
            self.variable_label.hide()
            self.variable_box.clear()
            self.variable_box.hide()
            
            self.is_variable = False
        
    def init_metros(self):
        
        #metros boxes
        self.box_filler = MetroNames()
        
        self.metroCountry = QtGui.QComboBox()
        self.metroCountry.addItems(self.box_filler.countries)
        self.metroCountry.currentIndexChanged.connect(self.newCountry)
        
        self.metroSt = QtGui.QComboBox()
        self.metroSt.addItems(self.box_filler.states)
        self.metroSt.currentIndexChanged.connect(self.newSt)
        
        self.metroCity = QtGui.QComboBox()
        self.metroCity.addItems(self.box_filler.metros)

        '''metros layout'''
        hboxMetroHeader = QtGui.QHBoxLayout()
        hboxMetroHeader.addWidget(QtGui.QLabel("Metro Information"))
        hboxMetroPlaceLabel = QtGui.QHBoxLayout()
        hboxMetroPlaceLabel.addWidget(QtGui.QLabel("Country"))
        hboxMetroPlaceLabel.addWidget(QtGui.QLabel("State"))
        hboxMetroPlace = QtGui.QHBoxLayout()
        hboxMetroPlace.addWidget(self.metroCountry)
        hboxMetroPlace.addWidget(self.metroSt)
        hboxMetroNameLabel = QtGui.QHBoxLayout()
        hboxMetroNameLabel.addWidget(QtGui.QLabel("Metro Name"))
        hboxMetroName = QtGui.QHBoxLayout()
        hboxMetroName.addWidget(self.metroCity)

        self.vboxMetro = QtGui.QVBoxLayout()
        self.vboxMetro.addLayout(hboxMetroHeader)
        self.vboxMetro.addLayout(hboxMetroPlaceLabel)
        self.vboxMetro.addLayout(hboxMetroPlace)
        self.vboxMetro.addLayout(hboxMetroNameLabel)
        self.vboxMetro.addLayout(hboxMetroName)

        self.metroBox = QtGui.QGroupBox()
        self.metroBox.setLayout(self.vboxMetro)
        self.metroBox.hide()

        self.metro_layout.addWidget(self.metroBox)
        
    def areMetros(self, now):
        if now == True:
            self.metroBox.show()
            self.is_metro = True
        elif now == False:
            self.metroBox.hide()
            self.is_metro = False

    def newCountry(self):
        source = self.sender()
        self.box_filler.newCountry(str(source.currentText()))
        self.metroSt.clear()
        self.metroCity.clear()
        self.metroSt.addItems(self.box_filler.states)

    def newSt(self):
        source = self.sender()
        self.box_filler.new_state(str(source.currentText()))
        self.metroCity.clear()
        self.metroCity.addItems(self.box_filler.metros)


class MetroNames():
    file_path = "\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\"
    conn = sqlite3.connect(file_path + "Database\\distributions.db")
    c = conn.cursor()
    countries = []
    states = []
    metros = []

    def __init__(self):
        for row in self.c.execute("SELECT DISTINCT country FROM metro_key"):
            self.countries.append(row[0])
        self.init_values()

    def init_values(self):
        for row in self.c.execute("SELECT DISTINCT state FROM metro_key WHERE country='United States'"):
            self.states.append(row[0])
        self.states.sort()

        #TODO: Possible HUGE bug below where self.states is NOT iterating. Thanks Chris A!
        for row in self.c.execute("SELECT DISTINCT city FROM metro_key WHERE state=?", [self.states[0]]):
            self.metros.append(row[0])
        self.metros.sort()

    def new_country(self, country):
        self.states = []
        for row in self.c.execute("SELECT DISTINCT state FROM metro_key WHERE country=?", [country]):
            self.states.append(row[0])
        self.states.sort()

    def new_state(self, state):
        self.metros = []
        for row in self.c.execute("SELECT DISTINCT city FROM metro_key WHERE state=?", [state]):
            self.metros.append(row[0])
        self.metros.sort()
        return


#creates date widgets and layouts, all date functions
class Dates(QtGui.QWidget):

    def __init__(self):

        super(Dates, self).__init__()
        self.makeDates()
        self.makeLayout()

    def makeDates(self):
        '''dateEdits and Labels'''
        self.startDate = QtGui.QDateEdit()
        self.startDate.setDate(QtCore.QDate.fromString('01.03.2010', 'MM.dd.yyyy'))

        self.endDate = QtGui.QDateEdit()
        self.endDate.setDate(QtCore.QDate.currentDate())

        self.startDateLabel = QtGui.QLabel()
        self.endDateLabel = QtGui.QLabel()

        self.endDate.dateChanged.connect(self.dateChange)
        self.startDate.dateChanged.connect(self.dateChange)
        self.switchDates(True)

    def makeLayout(self):
        '''layout'''

        hboxDateLabels = QtGui.QHBoxLayout()
        hboxDateLabels.addWidget(self.startDateLabel)
        hboxDateLabels.addStretch(1)
        hboxDateLabels.addWidget(self.endDateLabel)
        hboxDateEdits = QtGui.QHBoxLayout()
        hboxDateEdits.addWidget(self.startDate)
        hboxDateEdits.addStretch(1)
        hboxDateEdits.addWidget(self.endDate)

        self.dateLayout = QtGui.QVBoxLayout()
        self.dateLayout.addItem(hboxDateLabels)
        self.dateLayout.addItem(hboxDateEdits)

    def switchDates(self, weekly):
        if weekly is True:
            self.startDateLabel.setText('From Week starting ' + str(df.DateFunctions().end_week(self.startDate.date()
                                                                                                .toPyDate())))
            self.startDate.setDisplayFormat('MM.dd.yyyy')
            self.endDateLabel.setText('Through Week starting ' + str(df.DateFunctions().end_week(self.endDate.date()
                                                                                                 .toPyDate())))
            self.endDate.setDisplayFormat('MM.dd.yyyy')
        else:
            self.startDateLabel.setText('From 1st of ')
            self.startDate.setDisplayFormat('MM.yyyy')
            self.endDateLabel.setText('Through 31st of')
            self.endDate.setDisplayFormat('MM.yyyy')

    def dateChange(self):
        source = self.sender()
        if source.displayFormat() == u'MM.dd.yyyy':
            self.switchDates(True)
        else:
            self.switchDates(False)


class AnswerPopup(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Data")
        self.setGeometry(120, 50, 1000, 700)
        self.show()

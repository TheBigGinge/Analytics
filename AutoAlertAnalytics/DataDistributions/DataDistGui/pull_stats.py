import sqlite3

from PyQt4 import QtGui
from dateutil.relativedelta import relativedelta
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import DateFunctions.date_functions as df


"""
Chris Acree code below. BEWARE!
"""


class Solver():

    def __init__(self, index, start, end, other_var=0, country=0, state=0, city=0):
        self.v_box_data = None
        if index < 4:
            self.dist = WeeklyDist(index, df.DateFunctions().return_full_year_month_day(start), df.DateFunctions().return_full_year_month_day(end))
        elif index < 11:
            self.dist = MonthlyDist(index, df.DateFunctions().return_full_year_month_day(df.DateFunctions().start_month(start)),
                                    df.DateFunctions().return_full_year_month_day(df.DateFunctions().start_month(end)), other_var)
        elif index == 11:
            self.dist = RollupMetro(df.DateFunctions().return_full_year_month_day(df.DateFunctions().start_month(start)),
                                    df.DateFunctions().return_full_year_month_day(df.DateFunctions().start_month(end)), other_var,
                                    country, state, city)
        elif index == 12:
            self.dist = Metro(df.DateFunctions().return_full_year_month_day(df.DateFunctions().start_month(start)),
                              df.DateFunctions().return_full_year_month_day(df.DateFunctions().start_month(end)), country, state, city)

        self.dist.special()
        self.layout()
    
    def layout(self):
        self.v_box_data = QtGui.QVBoxLayout()

        self.v_box_data.addLayout(self.dist.hboxGraph)
        self.v_box_data.addLayout(self.dist.hboxTrend)
        self.v_box_data.addLayout(self.dist.hboxGraph2)
        self.v_box_data.addLayout(self.dist.hboxNums)
        

class Stats():
    file_path = "\\\\filer01\\public\\Data_Analytics\\Data_Distributions\\"

    #Functions and attributes common to all distributions
    conn = sqlite3.connect(file_path + "Database\\distributions.db")
    c = conn.cursor()

    def __init__(self):
        self.data_points_x = []
        self.data_points_y = []

        self.data_points_x_overall = []
        self.data_points_y_overall = []

        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)

        self.hboxGraph = QtGui.QHBoxLayout()
        self.hboxTrend = QtGui.QHBoxLayout()
        self.hboxNums = QtGui.QHBoxLayout()
        self.hboxGraph2 = QtGui.QHBoxLayout()

    def graph(self):

        if self.data_points_x is []:
            self.hboxGraph.addWidget(QtGui.QLabel("There are no data points for the selection."))
            return

        self.graph = self.fig.add_subplot(111)
        self.graph.fmt_xdata = matplotlib.dates.DateFormatter('%y-%m-%d')
        self.graph.plot_date(matplotlib.dates.date2num(self.data_points_x), self.data_points_y, '-')
        self.fig.autofmt_xdate()
        self.graph.set_ylabel('Profiles')
        self.graph.xaxis.set_ticks_position('bottom')
        self.graph.yaxis.set_ticks_position('left')
        self.hboxGraph.addWidget(self.canvas)

    def getMetroKey(self, country, state, city):
        self.c.execute("SELECT key FROM metro_key WHERE country='"+str(country)+
                       "' AND state='"+str(state)+"' AND city='"+str(city)+"'")
        key = str(self.c.fetchone()[0])
        return key

    def getData(self, query, start, weekly):
        #gets data from query, adds zeros to dates without entry
        if weekly is True:
            start = df.DateFunctions().end_week(start)
            for row in self.c.execute(query):
                if str(row[0]).startswith("9"):
                    #Keeping out values from before 2010
                    continue
                while df.DateFunctions().from_date(row[0]) != start and start < df.DateFunctions().from_date(row[0]):
                    #print(start)
                    #self.data_points_x.append(start)
                    #self.data_points_y.append(0)
                    start = start + relativedelta(days=+7)
                self.data_points_x.append(df.DateFunctions().from_date(row[0]))
                self.data_points_y.append(row[1])
                start = df.DateFunctions().from_date(row[0]) + relativedelta(days=+7)

        else:

            for row in self.c.execute(str(query)):
                while df.DateFunctions().from_date(row[0]) != start and start < df.DateFunctions().from_date(row[0]):
                    #self.data_points_x.append(start)
                    #self.data_points_y.append(0)
                    start = start + relativedelta(months=+1)
                self.data_points_x.append(df.DateFunctions().from_date(row[0]))
                self.data_points_y.append(row[1])
                start = df.DateFunctions().from_date(row[0]) + relativedelta(months=+1)

        '''puts data in box for user retrieval'''
        text = QtGui.QTextEdit()
        nums = ""
        for i in range(len(self.data_points_x)):
            nums = nums + str(self.data_points_x[i])+"\t"+str(self.data_points_y[i])+"\n"
        text.setText(nums)
        self.hboxNums.addWidget(QtGui.QLabel("Data points"))
        self.hboxNums.addWidget(text)


class WeeklyDist(Stats):
    
    def __init__(self, index, start, end):
        super(WeeklyDist, self).__init__()
        tables = ["active_profiles", "overall_profiles", "eac_weekly", "combined_salary_weekly"]
        self.table = tables[index]
        columns = ["profiles", "profiles", "median", "median"]
        self.column = columns[index]
        names = ['All Active Profiles', 'All Profiles', 'Median EAC', 'Median Combined Salary']

        #query = "SELECT * FROM " + self.table

        query = "SELECT date, " + self.column + " FROM " + self.table + " WHERE date >= " \
                + start + " AND date <= " + end + " ORDER BY date ASC"
        self.getData(query, df.DateFunctions().from_date(start), True)
        self.start = start
        self.end = end

        self.graph()
        self.fig.suptitle(names[index])

    def special(self):
        if self.table == 'active_profiles':
            all_profiles = WeeklyDist(1, self.start, self.end)
            self.hboxGraph2.addWidget(all_profiles.canvas)


class MonthlyDist(Stats):

    def __init__(self, index, start, end, other):
        super(MonthlyDist, self).__init__()

        tables = ["company_size", "degree_affinities", "naics_codes", "age_ranges", "onet_forty",
                  "years_experience", "rollups"]

        self.table = tables[index-4]
        columns = ["size_range", "level", "code", "age_range", "code",
                   "experience_range", "name"]
        self.column = columns[index-4]
        names = ['Company Size', 'Degree Level', 'NAICS Code',
                 'Years Old', 'ONET Code', 'Years Experience', 'Rollup']
        if index == 6:
            name = other[6:]
            other = other[:3]
        if index == 8:
            name = other[13:]
            other = other[:10]
        self.index = index
        self.other = other
        query = "SELECT date, profiles FROM " + self.table + " WHERE date >= " \
                + start + " AND date <= " + end + " AND " + self.column + "='" + other + \
                "' ORDER BY date ASC"
        self.getData(query, df.DateFunctions().from_date(start), False)
        self.start = start
        self.end = end
        
        self.graph()
        if index == 11:
            self.fig.suptitle(other + ' ' + names[index-4] + ' Profiles')
        elif index == 6 or index == 8:
            self.fig.suptitle(other+' ' + name + ' Profiles')
        else:
            self.fig.suptitle(names[index-4]+' ' + other + ' Profiles')

    def special(self):
        activeD = MonthlyDistOverall(self.index, self.start, self.end, self.other)

        self.hboxGraph2.addWidget(activeD.canvas)


class MonthlyDistOverall(Stats):

    def __init__(self, index, start, end, other):
        super(MonthlyDistOverall, self).__init__()
        tables = ["company_size_overall", "degree_affinities_overall", "naics_codes_overall",
                  "age_ranges_overall", "onet_forty_overall", "years_experience_overall", "rollups"]

        self.table = tables[index-4]
        columns = ["size_range", "level", "code", "age_range", "code",
                   "experience_range", "name"]
        self.column = columns[index-4]
        names = ['Company Size', 'Degree Level', 'NAICS Code',
                 'Years Old', 'ONET Code', 'Years Experience', 'Rollup']
        if index == 6:
            name = other[6:]
            other = other[:3]
        if index == 8:
            name = other[13:]
            other = other[:10]

        query = "SELECT date, profiles FROM " + self.table + " WHERE date >= " \
                + start + " AND date <= " + end + " AND " + self.column + "='" + other + \
                "' ORDER BY date ASC"
        self.getData(query, df.DateFunctions().from_date(start), False)
        self.start = start
        self.end = end

        self.graph()
        if index == 11:
            self.fig.suptitle(other + ' ' + names[index-4] + ' Profiles')
        elif index == 6 or index == 8:
            self.fig.suptitle(other+' ' + name + ' Profiles')
        else:
            self.fig.suptitle(names[index-4]+' ' + other + ' Profiles')


class RollupMetro(Stats):
    
    def __init__(self, start, end, rollup, country, state, city):
        super(RollupMetro, self).__init__()

        self.key = self.getMetroKey(country, state, city)
        query = "SELECT date, profiles FROM metro_rollups"+" WHERE date >= " + \
                start+" AND date <= "+end+" AND rollup='"+rollup + \
                "' AND metro_key="+self.key+" ORDER BY date ASC"
        self.getData(query, df.DateFunctions().from_date(start), False)
        self.graph()
        self.fig.suptitle(rollup+' Rollup in ' + city + ', ' + state +
                          ' Metro Area Profiles')
        
        self.start = start
        self.end = end
        self.rollup = rollup
        
    def special(self):
        metroD = Metro(self.start, self.end, metrokey=self.key)
        rollupD = MonthlyDistOverall(10, self.start, self.end, self.rollup)
        
        self.hboxGraph2.addWidget(metroD.canvas)
        self.hboxGraph2.addStretch(1)
        self.hboxGraph2.addWidget(rollupD.canvas)


class Metro(Stats):

    def __init__(self, start, end, country=0, state=0, city=0, metrokey=0):
        super(Metro, self).__init__()
        
        if metrokey == 0:
            key = self.getMetroKey(country, state, city)
        else:
            key = metrokey
        query= "SELECT date, profiles FROM metro_main WHERE date >= "+start+\
               " AND date <= "+end+" AND key="+key+" ORDER BY date ASC"
        self.getData(query, df.DateFunctions().from_date(start), False)
        self.graph()
        if city != 0:
            self.fig.suptitle(city + ', ' + state + ' Metro Area Profiles')
        else:
            self.fig.suptitle('All Metro Area Profiles')

        self.start = start
        self.end = end

    def special(self):
        activeD = WeeklyDist(0, self.start, self.end)

        self.hboxGraph2.addWidget(activeD.canvas)




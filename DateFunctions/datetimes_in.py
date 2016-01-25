import datetime
import calendar


class DateTimeFormats:

    def __init__(self):
        self.today = datetime.datetime.now()
        self.month = self.today.month
        self.year = self.today.year
        self.day = self.today.day

    def find_first_of_current_month(self, type_of_spacing = None):

        if type_of_spacing == None:
            return datetime.datetime(self.year, self.month, 1)
        else:
            return datetime.datetime(self.year, self.month, 1).strftime("%Y" + type_of_spacing +
                                                                     "%m" + type_of_spacing + "%d")

    def find_first_of_last_month(self):

        last_month = self.month - 1
        year = self.year

        if last_month == 0:
            last_month = 12
            year = self.year - 1

        return datetime.datetime(year, last_month, 1)

    def return_today_as_y_m(self, space):

        return self.today.strftime('%Y' + space + '%m')

    def return_last_month_as_y_m(self, space):

        month = self.month - 1
        year = self.year

        if month == 0:
            month = 12
            year -= 1

        return datetime.datetime(year, month, 1).strftime("%Y" + space + "%m")

    def return_today_as_y_m_d(self, space):

        return self.today.strftime("%Y" + space + "%m" + space + "%d")

    def find_first_of_month_x_years_ago(self, x):

        year = self.year - x

        return datetime.datetime(year, self.month, 1)

    def return_y_m_d_last_day_of_month(self, given_date=None, spacing=None):

        if given_date is not None:
            year = given_date.year()
            month = given_date.month()
        else:
            year = self.year
            month = self.month

        last_day = calendar.monthrange(year, month)[1]

        return datetime.datetime(year, month, last_day).strftime('%Y' + spacing + '%m' + spacing + '%d')

    @staticmethod
    def return_datetime_y_m_d_last_day_month(given_date):

        year = given_date.year()
        month = given_date.month()
        last_day = calendar.monthrange(year, month)[1]

        return datetime.datetime(year, month, last_day)

    @staticmethod
    def date_to_date_time(given_date):

        year = given_date.year()
        month = given_date.month()
        day = given_date.day()

        return datetime.datetime(year, month, day)

    def return_ymd_first_of_last_month(self, type_of_spacing):

        year = self.year
        month = self.month - 1
        day = 1

        if month == 0:
            month = 12
            year -= 1

        return datetime.datetime(year, month, day).strftime("%Y" + type_of_spacing + "%m" + type_of_spacing + "%d")

    def return_ymd_last_day_of_last_month(self, type_of_spacing = None):

        year = self.year
        month = self.month - 1

        if month == 0:
            month = 12
            year -= 1

        last_day = calendar.monthrange(year, month)[1]

        if type_of_spacing == None:

            return datetime.datetime(year, month, last_day)

        else:
            return datetime.datetime(year, month, last_day).strftime("%Y" + type_of_spacing +
                                                                     "%m" + type_of_spacing + "%d")

    def return_year_month_as_string(self, spacing):

        return datetime.datetime(self.year, self.month, 1).strftime("%Y" + spacing + "%m")
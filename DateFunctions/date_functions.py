import datetime


class DateFunctions:

    def __init__(self):
        self.today = datetime.datetime.now()

    @staticmethod
    def create_prior_date_by_days(start_date, days_ago):
        """
        Find the day that is x days before the start_date

        :param start_date:
            (datetime) The day you want to begin measuring from
        :param days_ago:
            (int) How many days prior to the start date you want
        :return:
            datetime value that is x days before the start_date
        """

        x_days_ago = start_date-datetime.timedelta(days=days_ago)

        return x_days_ago

    @staticmethod
    def create_prior_date_by_weeks(start_date, weeks_ago):
        """
        Find the day that is x weeks before the start_date
        """

        x_weeks_ago = start_date-datetime.timedelta(weeks=weeks_ago)

        return x_weeks_ago

    @staticmethod
    def datetime_to_string_y_m_d(target_date, type_of_spacing):
        """
        :param target_date:
            The date you want changed into year-month-day string format
        :param type_of_spacing:
            What you want to separate the year, month, day with.
            Examples: - or / or "" (2014-10-1) (2014/10/1) (20141001)
        :return:
            String of year, month, day
        """
        day = str(target_date.day)
        month = str(target_date.month)
        year = str(target_date.year)

        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month

        return year + type_of_spacing + month + type_of_spacing + day

    def find_most_recent_sunday(self):
        for i in xrange(0, 13):
            possible_sunday = self.today - datetime.timedelta(days=i)
            if possible_sunday.strftime("%A") == "Sunday":
                return possible_sunday

    def find_date_two_sundays_ago(self):
        total_sundays = 0
        for i in xrange(0, 13):
            possible_sunday = self.today - datetime.timedelta(days=i)
            if possible_sunday.strftime("%A") == "Sunday":
                total_sundays += 1
                if total_sundays == 2:
                    return possible_sunday

    def return_year_month_as_string(self, type_of_spacing):

        year = str(self.today.year)
        month = str(self.today.month)

        if len(month) == 1:
            month = "0" + month

        return year + type_of_spacing + month

    def return_ymd_first_of_the_current_month(self, type_of_spacing):

        year = str(self.today.year)
        month = str(self.today.month)

        if len(month) == 1:
            month = "0" + month

        return year + type_of_spacing + month + type_of_spacing + "01"

    def return_ymd_first_of_last_month(self, type_of_spacing):

        year = self.today.year
        month = self.today.month - 1

        if month == 0:
            month = 12
            year -= 1

        month = str(month)
        year = str(year)

        if len(month) == 1:
            month = "0" + month

        return year + type_of_spacing + month + type_of_spacing + "01"

    @staticmethod
    def return_full_year_month_day(day):
        """
        Designed to return a string date as a datetime of %Y/%m/%d.
        """
        assert isinstance(day, str), 'Day must be in string format'

        try:
            day = datetime.datetime.strptime(day, "%m/%d/%Y")

        except ValueError:
            raise AssertionError("Day must be in %m/%d/%Y format")

        return day.strftime("%Y%m%d")

    @staticmethod
    def end_week(t_date):
        """
        Chris Acree code
        """
        if t_date <= datetime.date(2010, 1, 2):
            return datetime.date(2010, 1, 2)
        elif t_date >= datetime.date.today():
            t_date = datetime.date.today()
        while t_date.weekday() != 5:
            t_date = t_date + datetime.timedelta(days=-1)
        return t_date

    @staticmethod
    def start_month(m_date):
        """
        Chris Acree code
        """
        return datetime.date(m_date.year, m_date.month, 1)

    @staticmethod
    def rob_date_return(date):

        assert isinstance(date, str), 'Day must be in string format'

        try:
            day = datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S %p")
            return day.strftime("%m/%d/%Y")
        except ValueError:
            day = date[:date.find(" ")]
            return day

    @staticmethod
    def splunk_date_format(date):

        assert isinstance(date, datetime.datetime), "Only datetime objects are accepted for the splunk dates."

        return_date = str(date.strftime("%Y-%m-%d"))

        return return_date  + "T12:00:00.000-07:00"
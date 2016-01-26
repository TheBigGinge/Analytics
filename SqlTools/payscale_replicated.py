import pyodbc


class SqlServer:
    """
    Make sure you're authenticated to PayScale's firewall
    or else this will fail.

    """

    def __init__(self, database):
        """
        :param self.query_string:
            This is your sql query. Write it as a sql query inside of triple quotes.
        :param database:
            The database you're querying (i.e. master, profiles, SiteStats, etc.).

        To get the out put iterate through the output and use iterator.return_value

        example:
            data = pr.SqlServer('SiteStats')
            query = some sql query returning ip_address and cnt
            data.set_query_string(query)

            data.initialize_connection()

            for row in data.return_results():
                print row.ip_address, row.cnt

        """
        self.data_base = database
        self.query_string = None
        self.conn = None
        self.cursor = None

    def set_query_string(self, query_string):

        self.query_string = query_string

    def initialize_connection(self):
        connection = 'DRIVER={SQL Server};SERVER=psdb03;DATABASE=' + self.data_base
        self.conn = pyodbc.connect(connection)
        self.cursor = self.conn.cursor()

    def return_results(self):

        self.cursor.execute(self.query_string)
        rows = self.cursor.fetchall()

        for row in rows:
            yield row
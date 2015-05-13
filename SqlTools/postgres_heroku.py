import psycopg2


class PostgresHeroku:

    def __init__(self):
        self.conn_string = None
        self.db = None
        self.user = None
        self.port = '5432'
        self.password = None
        self.host = None
        self.conn = None
        self.cursor = None

    def set_conn_string_from_parameters(self):
        assert self.db is not None, 'You left the parameter self.db as type None'
        assert self.user is not None, 'You left the parameter self.user as type None'
        assert self.password is not None, 'You left the parameter self.password as type None'
        assert self.host is not None, 'You left the parameter self.host as type None'

        self.conn_string = "host=" + self.host + " dbname=" + self.db + " port=" + self.port + " user=" + \
            self.user + " password=" + self.password

    def set_conn_string_from_string(self, string):
        self.conn_string = string

    def set_host(self, host):
        self.host = host

    def set_db(self, db):
        self.db = db

    def set_password(self, password):
        self.password = password

    def set_user(self, user):
        self.user = user

    def authenticate(self):
        if self.conn_string is not None:
            self.conn = psycopg2.connect(self.conn_string)
            self.cursor = self.conn.cursor()

    def sql_command(self, sql_string):
        self.cursor.execute(sql_string)

    def commit_and_close(self):
        self.conn.commit()
        self.conn.close()

    def fetchall(self):
        return self.cursor.fetchall()
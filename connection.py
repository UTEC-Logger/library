from sqlite3 import connect


class Connection:
    instance = None

    def __init__(self):
        if Connection.instance is None:
            Connection.instance = connect('sql.db')

            self.connection = Connection.instance

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

            Connection.instance = None

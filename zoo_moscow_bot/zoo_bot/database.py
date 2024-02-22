import psycopg2


class Database:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
            return True
        except psycopg2.Error as e:
            print("Unable to connect to the database.")
            print(e)
            return False

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        if self.connection is None:
            print("Not connected to the database.")
            return None

        cursor = self.connection.cursor()
        try:
            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except psycopg2.Error as e:
            print("Error executing query.")
            print(e)
            return None

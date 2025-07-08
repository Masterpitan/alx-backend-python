import sqlite3

# Context manager class to run a query and return result
class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
        self.conn = None
        self.result = None

    def __enter__(self):
        # Open DB connection
        self.conn = sqlite3.connect("users.db")
        cursor = self.conn.cursor()
        # Execute query with params
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the DB connection
        if self.conn:
            self.conn.close()
            print("Connection closed.")

# Use the context manager to run a parameterized query
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as result:
    print("Users over 25:")
    for row in result:
        print(row)

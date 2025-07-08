import sqlite3

# Class-based context manager for DB connection
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # Pass this to the with-block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("Connection closed.")

# Use the context manager to run a query
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Query Results:")
    for row in results:
        print(row)

import sqlite3
import functools
from datetime import datetime
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'query' in kwargs:
            query = kwargs.get['query']
        elif args:
            query = args[0]
        else:
            query = None
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"{timestamp} || SQL Query: {query}")
        else:
            print(f"{timestamp} || No query found")
        return func(*args, **kwargs)
    return wrapper
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close
    return results
# Fetch users while logging the query
users = fetch_all_users("query=SELECT * FROM users")

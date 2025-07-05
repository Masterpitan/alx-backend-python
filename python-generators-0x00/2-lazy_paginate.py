import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ALX_prodev")

def paginate_users(page_size, offset):
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

def lazy_paginate(page_size):
    offset = 0
    while True:  # One loop only
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Optional test
if __name__ == "__main__":
    for page in lazy_paginate(5):
        print("New Page:")
        for user in page:
            print(user)

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ALX_prodev")

def stream_user_ages():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # age is returned as a tuple (age,)
        yield age

    cursor.close()
    conn.close()

def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():  # ✅ First and only loop
        total_age += age
        count += 1

    average = total_age / count if count else 0
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ALX_prodev")

def stream_users_in_batches(batch_size):
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch  # yield remaining rows

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        filtered = [user for user in batch if user['age'] > 25]  # Loop 2 (list comp)
        yield filtered  # Yield only users over age 25

# Optional test run
if __name__ == "__main__":
    for filtered_batch in batch_processing(5):  # Loop 3
        print("Filtered batch:")
        for user in filtered_batch:
            print(user)

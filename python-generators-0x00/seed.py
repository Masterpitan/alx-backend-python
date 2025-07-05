import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import uuid
import csv
import os

from dotenv import load_dotenv
load_dotenv()

# Load DB credentials from .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ALX_prodev")

# Clean CSV and load it
def load_clean_csv(filepath):
    cleaned_rows = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            # Remove excessive quotes
            cleaned = [field.replace('"""', '').replace('"', '').strip() for field in row]
            if len(cleaned) == 3:
                cleaned_rows.append(cleaned)
    df = pd.DataFrame(cleaned_rows, columns=['name', 'email', 'age'])
    df = df.dropna()
    return df

# DB connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to MySQL server.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create DB
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()

# Connect to ALX_prodev
def connect_to_prodev():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print(f"Connected to {DB_NAME} database.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create table
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    print("Table user_data ensured.")
    cursor.close()

# Insert data
def insert_data(connection, df):
    cursor = connection.cursor()
    for _, row in df.iterrows():
        try:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = int(float(row['age']))  # ensure it's a number
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))
        except Exception as e:
            print(f"Insert error: {e}")
    connection.commit()
    print("Data inserted.")
    cursor.close()

# Main
def main():
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)
        df = load_clean_csv("user_data.csv")
        insert_data(db_conn, df)
        db_conn.close()

if __name__ == "__main__":
    main()

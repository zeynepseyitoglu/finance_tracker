import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        title TEXT,
        amount REAL,
        type TEXT)
               """)

conn.commit()
print("Table created successfully")

cursor.execute("""
    INSERT INTO transactions (title, amount, type)
    VALUES (%s, %s, %s)
""", ('Salary', 3000.00, 'income'))

conn.commit()
print("Transaction inserted!")

cursor.execute("SELECT * FROM transactions")
rows = cursor.fetchall()
print(rows)

cursor.close()
conn.close()
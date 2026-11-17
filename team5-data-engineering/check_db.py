
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

print("Checking database configuration...")
print("Host:", os.getenv("DB_HOST"))
print("Port:", os.getenv("DB_PORT"))
print("Database:", os.getenv("DB_NAME"))
print("User:", os.getenv("DB_USER"))
print("Password configured:", bool(os.getenv("DB_PASSWORD")))

try:
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user")
            print("Connection successful:", cursor.fetchone())

            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name = 'dataset_metadata'
            """)
            print("Metadata table:", cursor.fetchone())

except Exception as error:
    print("Connection failed:", type(error).__name__)
    print("Details:", error)

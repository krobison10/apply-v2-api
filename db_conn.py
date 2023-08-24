import os
import psycopg2.pool

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

try:
    connection_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=50,
        user=username,
        password=password,
        host=host,
        database=db_name,
    )
except:
    print("Failed to connect to database, terminating...")
    exit(3)

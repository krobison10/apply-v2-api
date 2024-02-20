import os
from dotenv import load_dotenv, find_dotenv
import psycopg2.pool

load_dotenv(find_dotenv())

username = "postgres"
password = os.environ.get("DB_PASSWORD")
host = "apply-dev-rds.cl6a4esq2qr9.us-west-2.rds.amazonaws.com"
db_name = "apply"

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

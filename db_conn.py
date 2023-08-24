import os
import psycopg2
import psycopg2.extras

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

try:
    connection = psycopg2.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
except:
    print('Failed to connect to database, terminating...')
    exit(3)
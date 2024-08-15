import sys
import psycopg2
from time import sleep

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(dbname="blog_app_db", user="postgres", password="qrc135zx", host="db")
            print("Database is ready!")
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Database is not ready. Waiting...")
            sleep(3)

if __name__ == '__main__':
    wait_for_db()

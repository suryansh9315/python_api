from psycopg2.extras import RealDictCursor
from .config import settings
import psycopg2
import time

def get_db():

    while True: 
        try:
            conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, user=settings.database_username, password=settings.database_password, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            return conn, cursor
        except Exception as error:
            print('Connection to Database Failed')
            print('Error: ', error)
            time.sleep(2)


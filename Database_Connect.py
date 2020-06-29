import psycopg2
from config import config
from psycopg2 import Error

class Database_Connect():

    def connect_database(temp = ""):
        conn = None
        try:
            params = config()

            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            cur = conn.cursor()
        except (Exception, Error) as error :
            print("Error is ", error)

        return cur, conn

    
    def select_query(query_val):
        database = Database_Connect()
        cur, conn = database.connect_database()
        cur.execute(query_val)

        select_result = cur.fetchall()

        if conn is not None:
            conn.close()
            print('Database connection closed.')

        return select_result

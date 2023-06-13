import pymysql
import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()


CRED = {
    'HOST':os.getenv('HOST'),
    'PORT':os.getenv('PORT'),
    'USER':os.getenv('USER'),
    'PASSWORD':os.getenv('PASSWORD'),
}


def db_conn():
    try:
        conn = pymysql.connect(host=CRED['HOST'], user=CRED['USER'], passwd=CRED['PASSWORD'])

        print("SUCCESSFUL CONNECTION")
        return conn.cursor()
 
    except mysql.connector.Error as e:
        print(f"CONNECTION FAILED - ERROR {e}")


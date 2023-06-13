import pymysql
from sqlalchemy import create_engine
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
        url = f"mysql+pymysql://{CRED['USER']}:{CRED['PASSWORD']}@{CRED['HOST']}:{CRED['PORT']}"
        engine = create_engine(url)
        print("SUCCESSFUL CONNECTION")
        return engine
 
    except mysql.connector.Error as e:
        print(f"CONNECTION FAILED - ERROR {e}")


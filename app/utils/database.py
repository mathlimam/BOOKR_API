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
        url = f"mysql+pymysql://{CRED['USER']}:{CRED['PASSWORD']}@{CRED['HOST']}:{CRED['PORT']}/bookrdb"
        engine = create_engine(url)
        return engine.connect()
 
    except mysql.connector.Error as e:
        print(f"CONNECTION FAILED - ERROR {e}")


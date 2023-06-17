from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
        url = f"mysql+pymysql://{CRED['USER']}:{CRED['PASSWORD']}@{CRED['HOST']}:{CRED['PORT']}/bookr"
        engine = create_engine(url)
        return engine.connect()
    
    except mysql.connector.Error as e:
        print(f"CONNECTION FAILED - ERROR {e}")

def db_session():
    engine = db_conn()
    db_session = sessionmaker(bind=engine)
    db = db_session()
    return db
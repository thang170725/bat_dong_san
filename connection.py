from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            database = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD')
        )
        return conn
    except Exception as e:
        print('lỗi kết nối cơ sở dữ liệu: ', e)
        return None

def fetch_dataframe(query):
    conn = get_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except:
        conn.close()
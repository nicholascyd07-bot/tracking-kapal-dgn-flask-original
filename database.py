#file koneksi ke database
import psycopg2

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'nodered_db',
    'user': 'postgres',
    'password': '6969'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)
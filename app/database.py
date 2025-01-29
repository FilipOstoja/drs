import mysql.connector
from mysql.connector import Error
import os

# MySQL URL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:admin@localhost/drs_restapi")

def get_db_connection():
    try:
        # Kreiraj konekciju prema bazi
        connection = mysql.connector.connect(
            host='localhost',
            database='drs_restapi',  # Tvoje ime baze
            user='root',  # Tvoj MySQL username
            password='admin'  # Tvoja lozinka za MySQL
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_db_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Database connection closed")

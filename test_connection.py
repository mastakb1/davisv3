import mysql.connector
from mysql.connector import Error
import os

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            connection.close()
    except Error as err:
        print(f"Error: {err}")

create_connection()

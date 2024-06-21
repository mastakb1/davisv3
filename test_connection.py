import mysql.connector
from mysql.connector import Error
import os

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('localhost'),
            user=os.getenv('root'),
            password=os.getenv(''),
            database=os.getenv('aw')
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            connection.close()
    except Error as err:
        print(f"Error: {err}")

create_connection()

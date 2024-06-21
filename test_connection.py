import mysql.connector
from mysql.connector import Error
import os

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),  # Replace with your actual host
            user=os.getenv('DB_USER', 'root'),      # Replace with your MySQL username
            password=os.getenv('DB_PASSWORD', ''),  # Replace with your MySQL password
            database=os.getenv('DB_NAME', 'aw')     # Replace with your MySQL database name
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            connection.close()
    except Error as err:
        print(f"Error: {err}")

create_connection()

import mysql.connector
import pandas as pd

def create_connection():
    return mysql.connector.connect(
        host="localhost",         
        user="root",            
        password="",      
        database="adventureworks_dw2"  
    
    )

def get_data_from_db(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="caregenic-db.cur0m2yuagx8.us-east-1.rds.amazonaws.com",
        user="admin",
        password="#Alina#321",
        database="caregenic_db"
    )
    return conn

import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="caregenic-db.cp0ym6yauvxr.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="#Alina#321",
        database="caregenic_db"
    )
    return conn

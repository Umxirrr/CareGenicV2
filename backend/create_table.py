from backend.db_connect import connect_db
from db_connect import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    phone VARCHAR(15),
    symptoms TEXT,
    disease VARCHAR(100),
    medicine VARCHAR(100),
    doctor VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
cursor.close()
conn.close()
print("✅ Table created successfully.")

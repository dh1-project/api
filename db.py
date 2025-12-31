import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )


def save_sensor_data(room_id, status=None):
    db = get_db()
    cursor = db.cursor()

    # Cek apakah room_id sudah ada
    cursor.execute(
        "SELECT * FROM status_detection_fall WHERE room_id = %s",
        (room_id,)
    )
    
    exist = cursor.fetchone()

    if exist:
        # Update jika sudah ada
        cursor.execute("""
            UPDATE status_detection_fall
            SET status = %s
            WHERE room_id = %s
        """, (status, room_id))
        print("[DB] UPDATED:", room_id, status)

    else:
        # Insert baru
        cursor.execute("""
            INSERT INTO status_detection_fall (room_id, status)
            VALUES (%s, %s)
        """, (room_id, status))
        print("[DB] INSERTED:", room_id, status)

    cursor.close()
    db.close()

import qrcode
import uuid
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


# --------------------------------
# DB Connection
# --------------------------------


def get_connection():
    """
    Returns a connection to the PostgreSQL database on Render.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not set in environment variables.")
    
    conn = psycopg2.connect(database_url)
    return conn


# --------------------------------
# Generate Unique QR ID
# --------------------------------


def generate_qr_id():
    return str(uuid.uuid4())  # random unique string


# --------------------------------
# Save QR Code in DB + Generate Image
# --------------------------------


def create_patient_qr(patient_id, save_path="qrcodes"):
    conn, cursor = None, None
    try:
        qr_id = generate_qr_id()

        # Insert into DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patient_qr (qr_id, patient_id, issued_date, status)
            VALUES (%s, %s, %s, %s)
        """, (qr_id, patient_id, datetime.now(), "Active"))
        conn.commit()

        # Make folder if not exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # Generate QR image
        qr = qrcode.make(qr_id)
        file_path = os.path.join(save_path, f"patient_{patient_id}.png")
        qr.save(file_path)

        print(f"[✔] QR Code generated for Patient {patient_id}: {file_path}")
        return qr_id, file_path
    except Exception as e:
        print(f"[X] Error generating QR. Try Again Later \n error: {e}")
        return None, None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# --------------------------------
# Fetch Patient by QR
# --------------------------------


def get_patient_by_qr(qr_id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.patient_id, p.name, p.gender, p.DOB, p.contact, p.address
            FROM patient_qr pq
            JOIN patient p ON pq.patient_id = p.patient_id
            WHERE pq.qr_id = %s AND pq.status = 'Active'
        """, (qr_id,))
        result = cursor.fetchone()
        if result:
            return {
                "patient_id": result[0],
                "name": result[1],
                "gender": result[2],
                "DOB": str(result[3]),
                "contact": result[4],
                "address": result[5]
            }
        else:
            return None
    except Exception as e:
        print(f"[X] Error fetching patient. Try Again Later \n error: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# --------------------------------
# Deactivate QR (if lost card)
# --------------------------------


def deactivate_qr(qr_id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE patient_qr SET status = 'Inactive' WHERE qr_id = %s", (qr_id,))
        conn.commit()
        print(f"[✔] QR {qr_id} deactivated.")
    except Exception as e:
        print(f"[X] Error deactivating QR. Try Again Later \n error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

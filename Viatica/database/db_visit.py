import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import database.db_qr as qr

load_dotenv()

def get_connection():
    """
    Returns a connection to the PostgreSQL database on Render.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not set in environment variables.")
    
    conn = psycopg2.connect(database_url)
    return conn


# -------------------------------
# Log a Visit
# -------------------------------


def log_visit(qr_id, doctor_id=None, department_id=None, service_id=None, status="Checked-In"):
    conn, cursor = None, None
    try:
        # ✅ Step 1: Fetch patient via QR
        patient = qr.get_patient_by_qr(qr_id)
        if not patient:
            print("[X] Invalid or inactive QR code.")
            return False
        patient_id = patient["patient_id"]
        # ✅ Step 2: Insert into visit_log
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO visit_log (patient_id, doctor_id, department_id, service_id, scan_time, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (patient_id, doctor_id, department_id, service_id, datetime.now(), status))
        conn.commit()
        print(f"[✔] Visit Logged For Patient {patient_id} (Doctor={doctor_id}, Dept={department_id}, Service={service_id})")
        return True
    except Exception as e:
        print(f"[X] Error Logging Visit. Try Again Later \n error: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------------------
# View All Visits (Admin)
# -------------------------------


def view_all_visits():
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.visit_id, p.name, d.name AS dept, doc.first_name AS fname, doc.last_name AS lname, s.service_name, v.scan_time, v.status
            FROM visit_log v
            LEFT JOIN patient p ON v.patient_id = p.patient_id
            LEFT JOIN department d ON v.department_id = d.department_id
            LEFT JOIN doctor doc ON v.doctor_id = doc.doctor_id
            LEFT JOIN services s ON v.service_id = s.service_id
            ORDER BY v.scan_time DESC
        """)
        results = cursor.fetchall()
        visits = []
        for row in results:
            visits.append({
                "visit_id": row[0],
                "patient_name": row[1],
                "department": row[2],
                "doctor": ((row[3] or '') + ' ' + (row[4] or '')).strip(),
                "service": row[5],
                "scan_time": str(row[6]),
                "status": row[7]
            })
        return visits
    except Exception as e:
        print(f"[X] Error Viewing Visits. Try Again Later \n error: {e}", )
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------------------
# Get All Visits by Patient
# -------------------------------


def get_visits_by_patient(patient_id):
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.visit_id, v.scan_time, v.status, d.name AS dept, doc.first_name AS fname, doc.last_name AS lname, s.service_name
            FROM visit_log v
            LEFT JOIN department d ON v.department_id = d.department_id
            LEFT JOIN doctor doc ON v.doctor_id = doc.doctor_id
            LEFT JOIN services s ON v.service_id = s.service_id
            WHERE v.patient_id = %s
            ORDER BY v.scan_time DESC
        """, (patient_id,))
        results = cursor.fetchall()
        visits = []
        for row in results:
            visits.append({
                "visit_id": row[0],
                "scan_time": str(row[1]),
                "status": row[2],
                "department": row[3],
                "doctor": ((row[4] or "" ) + " " + (row[5] or "" )),
                "service": row[6]
            })
        return visits
    except Exception as e:
        print(f"[X] Error Fetching Visits. Try Again Later \n error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

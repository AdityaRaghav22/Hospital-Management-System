import os
import psycopg2
from dotenv import load_dotenv

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

def insert_appointment(patient_id, doc_id, date, time, reason, status):
    conn = None
    cursor = None
    try:
        conn = get_connection()        # ✅ Establish DB connection
        cursor = conn.cursor()         # ✅ Create cursor for SQL execution
        # ✅ Insert query with parameter binding (safe against SQL injection)
        cursor.execute(
            """
                INSERT INTO appointment (patient_id, doctor_id, appointment_date , appointment_time , reason, status)
                VALUES (%s, %s, %s, %s, %s,%s)
            """, (patient_id, doc_id, date, time, reason, status)  # ✅ values passed as tuple
        )
        conn.commit()  # ✅ Commit transaction so the new appointment is saved
        print("[✓] Appointment created Successfully.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()  # ❌ Rollback if something goes wrong
        print(f"[X] Error creating A New appointment. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always clean up resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def delete_appointment(appointment_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()        # ✅ Establish DB connection
        cursor = conn.cursor()         # ✅ Create cursor for SQL execution
        # ✅ Insert query with parameter binding (safe against SQL injection)
        cursor.execute(
            """
                DELETE FROM appointment WHERE id = %s
            """,(appointment_id,)   # tuple required (id,)
        )
        conn.commit()   # ✅ Save changes permanently
        print(f"[✓] Appointment with id {appointment_id} deleted.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()   # ❌ Undo changes if an error occurs (safety)
        print(f"[X] Error Deleting Appointment With ID: '{appointment_id}'. Try Again Later \n Error: {e}")
        return False
    finally:
        # ✅ Always release resources
        if cursor: cursor.close()
        if conn: conn.close()
  
def update_appointment_date(appointment_id, new_date):
    update_field(appointment_id, "appointment_date", new_date)

def update_appointment_time(appointment_id, new_time):
    update_field(appointment_id, "appointment_time", new_time)

def update_appointment_reason(appointment_id, new_reason):
    update_field(appointment_id, "reason", new_reason)

def update_appointment_doc_id(appointment_id, new_doc_id):
    update_field(appointment_id, "doctor_id", new_doc_id)

def update_appointment_status(appointment_id, new_status):
    update_field(appointment_id, "status", new_status)

# ✅ Generic helper function to update any allowed field
def update_field(appointment_id, field, value):
    # Define which fields are allowed to be updated (safety check)
    allowed_fields = {"appointment_date", "appointment_time", "reason", "doctor_id", "status"}
    if field not in allowed_fields:
        raise ValueError("Invalid Field Name")  # Prevents SQL injection
    conn = None
    cursor = None
    try:
        conn = get_connection()   # Open DB connection
        cursor = conn.cursor()
        # ⚠️ Using f-string for column name is okay here since it's validated
        # But values (field value + appointment_id) must use parameter binding (%s)
        query = f"UPDATE appointment SET {field} = %s WHERE id = %s"
        cursor.execute(query, (value, appointment_id))  # Safe against SQL injection
        conn.commit()  # Save changes
        print(f"[✓] Updated {field} for appointment id: {appointment_id}")
        return True
    except Exception as e:
        if conn:
            conn.rollback()  # Rollback in case of error (data integrity)
        print(f"[X] Error Updating {field} For Appointment {appointment_id}. Try Again Later \n Error: {e}")
        return False

    finally:
        # Always close cursor & connection to avoid leaks
        if cursor: cursor.close()
        if conn: conn.close()

def view_patient_appointment(appointment_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Fetch the appointment details by ID using parameter binding (%s)
        if appointment_id:
            cursor.execute(
                """
                    SELECT 
                    a.id AS appointment_id,
                    p.name AS patient_name,
                    p.age AS patient_age,
                    d.name AS doctor_name,
                    d.specialization,
                    a.appointment_date,
                    a.appointment_time,
                    a.reason,
                    a.status
                FROM appointment a
                JOIN patient p ON a.patient_id = p.id
                JOIN doctor d ON a.doctor_id = d.id
                where a.id = %s
                """, (appointment_id,)   # tuple required: (appointment_id,)
            )
        result = cursor.fetchone()
        if result is None:
            return None
        appointment_id, pat_name, pat_age, doc_name, doc_specialization, appointment_date , appointment_time , reason, status = result
        appointment_details = {
            "appointment_id" : appointment_id,
            "patient_name" : pat_name,
            "patient_age" : pat_age,
            "doctor_name" : doc_name,
            "doctor_specialization" : doc_specialization,
            "appointment_date" : appointment_date,
            "appointment_time" : appointment_time,
            "reason" : reason,
            "status": status
        }
        return appointment_details
    except Exception as e:
        # ❌ If something goes wrong, log error and return None (safe fallback)
        if conn:
            print(f"[X] Error Fetching Info For Patient's Appointment. Try Again Later \n Error: {e}")
        return None
    finally:
        # ✅ Ensure resources are always closed (important for production)
        if cursor: cursor.close()
        if conn: conn.close()

def view_patient_appointments(patient_id):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all appointments joined with patient + doctor details
        cursor.execute(
            """
                SELECT 
                a.id AS appointment_id,
                p.name AS patient_name,
                p.age AS patient_age,
                d.name AS doctor_name,
                d.specialization,
                a.appointment_date,
                a.appointment_time,
                a.reason,
                a.status
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
            where a.patient_id = %s
            ORDER BY a.appointment_date, a.appointment_time LIMIT 100 OFFSET 0
            """,(patient_id,)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "appointment_id" : appointment_id,
            "patient_name" : pat_name,
            "patient_age" : pat_age,
            "doctor_name" : doc_name,
            "doctor_specialization" : doc_specialization,
            "appointment_date" : appointment_date ,
            "appointment_time" : appointment_time,
            "reason" : reason,
            "status": status
            }
            for appointment_id, pat_name, pat_age, doc_name, doc_specialization, appointment_date , appointment_time, reason, status in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Patient's Appointment Info. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_all_appointment():
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all appointments joined with patient + doctor details
        cursor.execute(
            """
                SELECT 
                a.id AS appointment_id,
                p.name AS patient_name,
                p.age AS patient_age,
                d.name AS doctor_name,
                d.specialization,
                a.appointment_date,
                a.appointment_time,
                a.reason,
                a.status
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
            ORDER BY a.appointment_date, a.appointment_time LIMIT 100 OFFSET 0
            """
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "appointment_id" : appointment_id,
            "patient_name" : pat_name,
            "patient_age" : pat_age,
            "doctor_name" : doc_name,
            "doctor_specialization" : doc_specialization,
            "appointment_date" : appointment_date ,
            "appointment_time" : appointment_time,
            "reason" : reason,
            "status": status

            }
            for appointment_id, pat_name, pat_age, doc_name, doc_specialization, appointment_date , appointment_time, reason, status in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching All Appointments. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_doctor_appointments(doctor_id):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all appointments joined with patient + doctor details
        cursor.execute(
            """
                SELECT 
                a.id AS appointment_id,
                p.name AS patient_name,
                p.age AS patient_age,
                d.name AS doctor_name,
                d.specialization,
                a.appointment_date,
                a.appointment_time,
                a.reason,
                a.status
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
            where a.doctor_id = %s
            ORDER BY a.appointment_date, a.appointment_time LIMIT 100 OFFSET 0
            """,(doctor_id,)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "appointment_id" : appointment_id,
            "patient_name" : pat_name,
            "patient_age" : pat_age,
            "doctor_name" : doc_name,
            "doctor_specialization" : doc_specialization,
            "appointment_date" : appointment_date ,
            "appointment_time" : appointment_time,
            "reason" : reason,
            "status": status
            }
            for appointment_id, pat_name, pat_age, doc_name, doc_specialization, appointment_date , appointment_time, reason, status in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Doctor's Appointment. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_appointment_by_date(date):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all appointments joined with patient + doctor details
        cursor.execute(
            """
                SELECT 
                a.id AS appointment_id,
                p.name AS patient_name,
                p.age AS patient_age,
                d.name AS doctor_name,
                d.specialization,
                a.appointment_date,
                a.appointment_time,
                a.reason,
                a.status
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
            where a.appointment_date = %s
            ORDER BY a.appointment_date, a.appointment_time LIMIT 100 OFFSET 0
            """,(date,)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "appointment_id" : appointment_id,
            "patient_name" : pat_name,
            "patient_age" : pat_age,
            "doctor_name" : doc_name,
            "doctor_specialization" : doc_specialization,
            "appointment_date" : appointment_date ,
            "appointment_time" : appointment_time,
            "reason" : reason,
            "status": status
            }
            for appointment_id, pat_name, pat_age, doc_name, doc_specialization, appointment_date , appointment_time, reason, status in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Appointments By Date. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_appointment_by_status(status):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all appointments joined with patient + doctor details
        cursor.execute(
            """
                SELECT 
                a.id AS appointment_id,
                p.name AS patient_name,
                p.age AS patient_age,
                d.name AS doctor_name,
                d.specialization,
                a.appointment_date,
                a.appointment_time,
                a.reason,
                a.status
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
            where a.status = %s
            ORDER BY a.appointment_date, a.appointment_time LIMIT 100 OFFSET 0
            """,(status,)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "appointment_id" : appointment_id,
            "patient_name" : pat_name,
            "patient_age" : pat_age,
            "doctor_name" : doc_name,
            "doctor_specialization" : doc_specialization,
            "appointment_date" : appointment_date ,
            "appointment_time" : appointment_time,
            "reason" : reason,
            "status": status
            }
            for appointment_id, pat_name, pat_age, doc_name, doc_specialization, appointment_date , appointment_time, reason, status in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Appointments By Status. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def count_appointments():
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all appointments joined with patient + doctor details
        cursor.execute(
            """
                SELECT count(id) as total_appointment from appointment
            """
        )
        rows = cursor.fetchone()
        return rows[0] if rows else 0
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Count Of Total Appointment. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def count_patient_by_status(status):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all appointments joined with patient + doctor details
        cursor.execute(
            """
                SELECT count(id) as total_appointment 
                FROM appointment
                WHERE status = %s
            """,(status, )
        )
        rows = cursor.fetchone()
        return rows[0] if rows else 0
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Count Of Total Appointment By Status. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def appointment_exists_patient_id(patient_id, date, time):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any patient exists with the given contact
        cursor.execute("""
                            SELECT id 
                            FROM appointment
                            WHERE patient_id = %s 
                                AND appointment_date = %s 
                                AND appointment_time = %s 
                                AND status = 'Scheduled'
                       """, (patient_id, date, time))
        # ✅ fetchone() returns a row if found, otherwise None
        row = cursor.fetchone()
        if row:
            print(f"Appointment Exists With Patient Id: {patient_id}")
            return True
        else:
            print(f"No Appointment Found For Patient Id: {patient_id}")
            return False
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Appoitnment: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def appointment_exists_id(appointment_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any patient exists with the given contact
        cursor.execute("""
                            SELECT id 
                            FROM appointment
                            WHERE patient_id = %s 
                                AND appointment_date = %s 
                                AND appointment_time = %s 
                                AND status = 'Scheduled'
                       """, (appointment_id,))
        # ✅ fetchone() returns a row if found, otherwise None
        row = cursor.fetchone()
        if row:
            print(f"Appointment Exists With Appointment Id: {appointment_id}")
            return True
        else:
            print(f"No Appointment Found For Appointment Id: {appointment_id}")
            return False
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Appoitnment: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

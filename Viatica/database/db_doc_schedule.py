import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

def add_availability(id, doc_id,date,day_of_week, start_time, end_time, slot_duration):
    conn = None
    cursor = None
    try:
        conn = get_connection()        # ✅ Establish DB connection
        cursor = conn.cursor()         # ✅ Create cursor for SQL execution
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")

        while start < end:
            cursor.execute(
                """
                INSERT IGNORE INTO doctor_availability (id, doctor_id, available_date, available_time, day_of_week, is_booked)
                VALUES (%s, %s, %s, %s, %s, FALSE)
                """,
                (id, doc_id, date, start.time(), day_of_week)
            )
            start += timedelta(minutes=slot_duration)
        conn.commit()  # ✅ Commit transaction so the new Doctors is saved
        print("[✓] Availability Added Successfully.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()  # ❌ Rollback if something goes wrong
        print(f"[X] Error Inserting A New Availability. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always clean up resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def delete_slot(availability_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()       # ✅ Establish DB connection
        cursor = conn.cursor()        # ✅ Create cursor for executing SQL commands
        # ✅ Execute delete query safely using parameter binding (%s)
        cursor.execute(
            """
                DELETE FROM doctor_availability WHERE id = %s
            """, (availability_id, )   # tuple required (id, start_time)
        )
        conn.commit()   # ✅ Save changes permanently
        print(f"[✓] Availability with id {availability_id} deleted.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()   # ❌ Undo changes if an error occurs (safety)
        print(f"[X] Error Deleting Availability with id: '{availability_id}'. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always release resources
        if cursor: cursor.close()
        if conn: conn.close()

def delete_slot_with_doc_id(doc_id, date, start_time = None):
    conn = None
    cursor = None
    try:
        conn = get_connection()       # ✅ Establish DB connection
        cursor = conn.cursor()        # ✅ Create cursor for executing SQL commands
        # ✅ Execute delete query safely using parameter binding (%s)
        if start_time:
            cursor.execute(
                """
                    DELETE FROM doctor_availability WHERE doctor_id = %s AND available_date = %s AND available_time = %s
                """, (doc_id, date, start_time)   # tuple required (doc_id, date, start_time)
            )
        else:
            cursor.execute(
                """
                    DELETE FROM doctor_availability WHERE doctor_id = %s AND available_date = %s
                """, (doc_id, date)   # tuple required (doc_id, date)
            )
        conn.commit()   # ✅ Save changes permanently
        if cursor.rowcount > 0:
            if start_time:
                print(f"[✓] Slot on {date} at {start_time} for doctor {doc_id} deleted.")
            else:
                print(f"[✓] All slots for doctor {doc_id} on {date} deleted.")
            return True
        else:
            print("[!] No matching Slots Found To Delete.")
            return False
    except Exception as e:
        if conn:
            conn.rollback()   # ❌ Undo changes if an error occurs (safety)
        print(f"[X] Error Deleting Availability With doc_id and date: '{doc_id}' '{date}'. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always release resources
        if cursor: cursor.close()
        if conn: conn.close()

def mark_slot_booked(availability_id, date, start_time):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                UPDATE doctor_availability SET is_booked = TRUE
                WHERE id = %s
            """, (availability_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            print(f"[✓] Slot {availability_id} On {date} At {start_time} Marked As Booked.")
            return True
        else:
            print(f"[!] No Matching Slot Found For {availability_id} On {date} At {start_time}.")
            return False
    except Exception as e:
        if conn:
            conn.rollback()   # ❌ Undo changes if an error occurs (safety)
        print(f"[X] Error Booking Availability with Appointment_id and start_time: '{availability_id}'---> '{date}': '{start_time}'. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always release resources
        if cursor: cursor.close()
        if conn: conn.close()

def mark_slot_free(availability_id, date, start_time):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                UPDATE doctor_availability SET is_booked = FALSE
                WHERE id = %s
            """, (availability_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            print(f"[✓] Slot {availability_id} On {date} At {start_time} Marked As Free.")
            return True
        else:
            print(f"[!] No Matching Slot Found For {availability_id} On {date} At {start_time}.")
            return False
    except Exception as e:
        if conn:
            conn.rollback()   # ❌ Undo changes if an error occurs (safety)
        print(f"[X] Error Cancelling Availability with Appointment_id and start_time: '{availability_id}'---> '{date}': '{start_time}'. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always release resources
        if cursor: cursor.close()
        if conn: conn.close()

def view_all_availability_for_doc(doc_id, limit = 100, offset = 0):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all doctors_availability (id, doctor_id, available_date, available_time, day_of_week, is_booked)
        cursor.execute(
            """
                SELECT id, doctor_id, available_date, available_time, day_of_week, is_booked
                FROM doctor_availability
                WHERE doctor_id = %s
                ORDER BY id LIMIT %s OFFSET %s
            """,(doc_id, limit, offset)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "id" : id,
            "doctor_id" :doctor_id ,
            "available_date" : available_date,
            "available_time" : available_time,
            "day_of_week" : day_of_week,
            "is_booked" : is_booked
            }
            for id, doctor_id, available_date, available_time, day_of_week, is_booked in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Availability Info: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_day_schedule(doc_id, available_date):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all doctors_availability (id, doctor_id, available_date, available_time, day_of_week, is_booked)
        cursor.execute(
            """
                SELECT id, doctor_id, available_date, available_time, day_of_week, is_booked
                FROM doctor_availability
                WHERE doctor_id = %s AND available_date = %s
                
            """,(doc_id, available_date)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "id" : id,
            "doctor_id" :doctor_id ,
            "available_date" : available_date,
            "available_time" : available_time,
            "day_of_week" : day_of_week,
            "is_booked" : is_booked
            }
            for id, doctor_id, available_date, available_time, day_of_week, is_booked in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Availability Info: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_free_slots(doc_id, available_date):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all doctors_availability (id, doctor_id, available_date, available_time, day_of_week, is_booked)
        cursor.execute(
            """
                SELECT id, doctor_id, available_date, available_time, day_of_week, is_booked
                FROM doctor_availability
                WHERE doctor_id = %s AND available_date = %s AND is_booked = FALSE
                
            """,(doc_id, available_date)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "id" : id,
            "doctor_id" :doctor_id ,
            "available_date" : available_date,
            "available_time" : available_time,
            "day_of_week" : day_of_week,
            "is_booked" : is_booked
            }
            for id, doctor_id, available_date, available_time, day_of_week, is_booked in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Availability Info: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_booked_slots(doc_id, available_date):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all doctors_availability (id, doctor_id, available_date, available_time, day_of_week, is_booked)
        cursor.execute(
            """
                SELECT id, doctor_id, available_date, available_time, day_of_week, is_booked
                FROM doctor_availability
                WHERE doctor_id = %s AND available_date = %s AND is_booked = TRUE
                
            """,(doc_id, available_date)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "id" : id,
            "doctor_id" :doctor_id ,
            "available_date" : available_date,
            "available_time" : available_time,
            "day_of_week" : day_of_week,
            "is_booked" : is_booked
            }
            for id, doctor_id, available_date, available_time, day_of_week, is_booked in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Availability Info: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_all_availability():
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all doctors_availability (id, doctor_id, available_date, available_time, day_of_week, is_booked)
        cursor.execute(
            """
                SELECT id, doctor_id, available_date, available_time, day_of_week, is_booked
                FROM doctor_availability
            """
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "id" : id,
            "doctor_id" :doctor_id ,
            "available_date" : available_date,
            "available_time" : available_time,
            "day_of_week" : day_of_week,
            "is_booked" : is_booked
            }
            for id, doctor_id, available_date, available_time, day_of_week, is_booked in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Availability Info: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def availability_exists(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any patient exists with the given contact
        cursor.execute("SELECT id FROM availability WHERE id = %s", (id,))
        # ✅ fetchone() returns a row if found, otherwise None
        print(f"Availability Exists With Id: {id}")
        return cursor.fetchone() is not None
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Availability: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def availability_exists_doc(id, date, start_time):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any patient exists with the given contact
        cursor.execute("""
                            SELECT id 
                            FROM doctor_availability
                            WHERE patient_id = %s 
                                AND available_date = %s 
                                AND available_time = %s 
                       """, (id, date, start_time))
        # ✅ fetchone() returns a row if found, otherwise None
        row = cursor.fetchone()
        if row:
            print(f"Slot Exists With Doctor Id: {id}")
            return True
        else:
            print(f"No Slot Found For Doctor Id: {id}")
            return False
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Slot: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()
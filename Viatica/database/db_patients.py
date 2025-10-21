import os
import psycopg2
from dotenv import load_dotenv
from config import mydb
import pymysql



load_dotenv()

# def get_connection():
#     """
#     Returns a connection to the PostgreSQL database on Render.
#     """
#     database_url = os.getenv("DATABASE_URL")
#     if not database_url:
#         raise ValueError("DATABASE_URL not set in environment variables.")
    
#     conn = psycopg2.connect(database_url)
#     return conn

def get_connection():
    return pymysql.connect(**mydb)

# -------------------
# INSERT
# -------------------


def insert_patient(id, name, gender, age, blood_group, contact):
    conn = None
    cursor = None
    try:
        conn = get_connection()        # ✅ Establish DB connection
        cursor = conn.cursor()         # ✅ Create cursor for SQL execution
        # ✅ Insert query with parameter binding (safe against SQL injection)
        cursor.execute(
            """
                INSERT INTO patient (id, name, gender, age, blood_group, contact) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id, name, gender, age, blood_group, contact)  # ✅ values passed as tuple
        )
        conn.commit()  # ✅ Commit transaction so the new patient is saved
        print("[✓] Patient added successfully.")
    except Exception as e:
        if conn:
            conn.rollback()  # ❌ Rollback if something goes wrong
        print(f"[X] Error Inserting A New Patient. Try Again Later \n error: {e}")
    finally:    
        # ✅ Always clean up resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# DELETE
# -------------------


def delete_patients(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()       # ✅ Establish DB connection
        cursor = conn.cursor()        # ✅ Create cursor for executing SQL commands
        # ✅ Execute delete query safely using parameter binding (%s)
        cursor.execute(
            """
                DELETE FROM patient WHERE id = %s
            """, (id,)   # tuple required (id,)
        )
        conn.commit()   # ✅ Save changes permanently
        print(f"[✓] Patient with id {id} deleted.")
    except Exception as e:
        if conn:
            conn.rollback()   # ❌ Undo changes if an error occurs (safety)
        print(f"[X] Error Deleting Patient with id: '{id}'. Try Again Later \n error: {e}")
    finally:
        # ✅ Always release resources
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# Update
# -------------------


# Individual update functions for each patient attribute
def update_patient_name(patient_id, new_name):
    # Calls helper function to update only the "name" field
    update_field(patient_id, "name", new_name)

def update_patient_gender(patient_id, new_gender):
    # Calls helper function to update only the "gender" field
    update_field(patient_id, "gender", new_gender)

def update_patient_age(patient_id, new_age):
    # Calls helper function to update only the "age" field
    update_field(patient_id, "age", new_age)

def update_patient_contact(patient_id, new_contact):
    # Calls helper function to update only the "contact" field
    update_field(patient_id, "contact", new_contact)

def update_patient_blood_group(patient_id, new_bg):
    # Calls helper function to update only the "blood_group" field
    update_field(patient_id, "blood_group", new_bg)

# ✅ Generic helper function to update any allowed field
def update_field(patient_id, field, value):
    # Define which fields are allowed to be updated (safety check)
    allowed_fields = {"name", "gender", "age", "blood_group", "contact"}
    if field not in allowed_fields:
        raise ValueError("Invalid Field Name")  # Prevents SQL injection
    conn = None
    cursor = None
    try:
        conn = get_connection()   # Open DB connection
        cursor = conn.cursor()
        # ⚠️ Using f-string for column name is okay here since it's validated
        # But values (field value + patient_id) must use parameter binding (%s)
        query = f"UPDATE patient SET {field} = %s WHERE id = %s"
        cursor.execute(query, (value, patient_id))  # Safe against SQL injection
        conn.commit()  # Save changes
        print(f"[✓] Updated {field} for patient {patient_id}")
    except Exception as e:
        if conn:
            conn.rollback()  # Rollback in case of error (data integrity)
        print(f"[X] Error updating {field} for patient {patient_id}: {e}")
    finally:
        # Always close cursor & connection to avoid leaks
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# View One Patient
# -------------------


def view_patient(patient_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Fetch the patient details by ID using parameter binding (%s)
        cursor.execute(
            """
                SELECT id, name, gender, age, blood_group, contact 
                FROM patient
                WHERE id = %s
            """, (patient_id,)   # tuple required: (patient_id,)
        )
        result = cursor.fetchone()   # ✅ Returns single row or None
        if result is None:
            return None  # No patient found with given ID
        # ✅ Unpack tuple directly into variables
        id, name, gender, age, blood_group, contact = result
        # ✅ Ensure 'age' is stored as integer, fallback to None if invalid
        try:
            age = int(age)
        except (ValueError, TypeError):
            print(f"[X] Invalid age value in DB: {age} for patient id: {patient_id}")
            age = None
        # ✅ Ensure 'contact' is stored as integer, fallback to None if invalid
        try:
            contact = int(contact)
        except (ValueError, TypeError):
            print(f"[X] Invalid contact value in DB: {contact} for patient id: {patient_id}")
            contact = None
        # ✅ Construct a clean dictionary for returning data
        patient_details = {
            "id": id,
            "name": name,
            "gender": gender,
            "age": age,
            "blood_group": blood_group,
            "contact": contact
        }
        return patient_details
    except Exception as e:
        # ❌ If something goes wrong, log error and return None (safe fallback)
        if conn:
            print(f"[X] Error Fetching Info For Patient {patient_id}: {e}")
        return None
    finally:
        # ✅ Ensure resources are always closed (important for production)
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# View All Patient
# -------------------



def view_all_patients():
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all patients (id, name, gender, age, contact)
        cursor.execute(
            """
                SELECT id, name, gender, age, blood_group, contact
                FROM patient
                ORDER BY id LIMIT 100 OFFSET 0
            """
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
                "id": id,
                "name": name,
                "gender": gender,
                "age": age,
                "blood_group": blood_group,
                "contact": contact
            }
            for id, name, gender, age, blood_group, contact in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Info: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# -------------------
# Count Patient
# -------------------


def count_patients():
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Execute COUNT query to get total number of patients
        cursor.execute("SELECT COUNT(*) FROM patient")
        # ✅ Fetch result (always returns a single row with one value)
        return cursor.fetchone()[0]
    except Exception as e:
        # ❌ If something goes wrong, log the error but don’t crash program
        if conn:
            print(f"[X] Error Counting Patients: {e}")
        return None  # ✅ Safe fallback in case of error
    finally:
        # ✅ Ensure resources are always closed to prevent memory leaks
        if cursor: cursor.close()
        if conn: conn.close()
    
def count_patients_by_gender():
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Count patients grouped by gender
        cursor.execute(
                """
                    SELECT gender, COUNT(*) as Total
                    FROM patient
                    GROUP BY gender
                    ORDER BY COUNT(*) ASC 
                """
            )
        # ✅ Fetch all rows (list of tuples: [(blood_group, count), ...])
        results = cursor.fetchall() 
        # ✅ Convert to dict: {"male": 12, "female": 7 }
        return {row[0]: row[1] for row in results} if results else {} # ✅ Safe fallback if no rows
    except Exception as e:
        # ❌ If something goes wrong, log the error but don’t crash program
        if conn:
            print(f"[X] Error Counting Patients By Gender: {e}")
        return {}  # ✅ Safe fallback in case of error
    finally:
        # ✅ Ensure resources are always closed to prevent memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def count_patients_by_blood_group():
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Count patients grouped by blood group
        cursor.execute(
                """
                    SELECT blood_group, COUNT(*) as Total
                    FROM patient
                    GROUP BY blood_group
                    ORDER BY COUNT(*) ASC 
                """
            )
        # ✅ Fetch all rows (list of tuples: [(blood_group, count), ...])
        results = cursor.fetchall() 
        # ✅ Convert to dict: {"A+": 12, "B+": 7, ...}
        return {row[0]: row[1] for row in results} if results else {} # ✅ Safe fallback if no rows
    except Exception as e:
        # ❌ If something goes wrong, log the error but don’t crash program
        if conn:
            print(f"[X] Error Counting Patients By Blood Group: {e}")
        return {}  # ✅ Safe fallback in case of error
    finally:
        # ✅ Ensure resources are always closed to prevent memory leaks
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# Check Existence Of Patient
# -------------------


def patient_exists_contact(contact):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any patient exists with the given contact
        cursor.execute("SELECT id FROM patient WHERE contact = %s", (contact,))
        # ✅ fetchone() returns a row if found, otherwise None
        return cursor.fetchone() is not None
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Patient: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def patient_exists_id(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any patient exists with the given contact
        cursor.execute("SELECT id FROM patient WHERE id = %s", (id,))
        # ✅ fetchone() returns a row if found, otherwise None
        return cursor.fetchone() is not None
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Patient: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

# -------------------
# Search Patients
# -------------------


def search_patient_by_contact(contact):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Fetch the patient details by contact using parameter binding (%s)
        cursor.execute(
            """
                SELECT id, name, gender, age, blood_group, contact 
                FROM patient
                WHERE contact = %s
            """, (contact,)   # tuple required: (patient_id,)
        )
        result = cursor.fetchone()   # ✅ Returns single row or None
        if result is None:
            return None  # No patient found with given ID
        # ✅ Unpack tuple directly into variables
        id, name, gender, age, blood_group, contact = result
        # ✅ Ensure 'age' is stored as integer, fallback to None if invalid
        try:
            age = int(age)
        except (ValueError, TypeError):
            print(f"[X] Invalid age value in DB: {age} for id: {id}")
            age = None
        # ✅ Construct a clean dictionary for returning data
        patient_details = {
            "id": id,
            "name": name,
            "gender": gender,
            "age": age,
            "blood_group": blood_group,
            "contact": contact
        }
        return patient_details
    except Exception as e:
        # ❌ If something goes wrong, log error and return None (safe fallback)
        if conn:
            print(f"[X] Error Fetching Info For Patient With Contact Number {contact}: {e}")
        return None
    finally:
        # ✅ Ensure resources are always closed (important for production)
        if cursor: cursor.close()
        if conn: conn.close()

def search_by_blood_group(blood_group):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish connection to the database
        cursor = conn.cursor()    # ✅ Create a cursor object for executing SQL queries
        # ✅ Run query to fetch patient details where blood group matches
        cursor.execute(
            """
                SELECT id, name, gender, age, blood_group, contact 
                FROM patient
                WHERE blood_group = %s
            """, (blood_group,)   # ✅ Pass parameter safely using tuple (avoids SQL injection)
        )
        results = cursor.fetchall()   # ✅ Get all matching rows (list of tuples)
        if not results:
            return []  # ✅ Return empty list if no patients found for this blood group
        patients = []   # ✅ Prepare a list to store formatted patient records
        for row in results:
            id, name, gender, age, blood_group_db, contact = row   # ✅ Unpack row fields
            # ✅ Ensure age is always an integer (handle bad/invalid DB values safely)
            try:
                age = int(age)
            except (ValueError, TypeError):
                print(f"[X] Invalid age value in DB: {age} for id: {id}")
                age = None   # ✅ If invalid, set to None instead of crashing
            # ✅ Build dictionary for patient record
            patients.append({
                "id": id,
                "name": name,
                "gender": gender,
                "age": age,
                "blood_group": blood_group_db,
                "contact": contact
            })
        return patients   # ✅ Return list of patient dictionaries
    except Exception as e:
        # ❌ Handle any errors safely and log useful info
        if conn:
            print(f"[X] Error fetching patients with blood group {blood_group}: {e}")
        return None   # ✅ Return None if an error occurs (caller can handle this)
    finally:
        # ✅ Ensure resources are always released properly
        if cursor: cursor.close()
        if conn: conn.close()

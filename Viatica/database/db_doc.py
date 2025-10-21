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



# -------------------
# INSERT
# -------------------


def insert_doc(id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()        # ✅ Establish DB connection
        cursor = conn.cursor()         # ✅ Create cursor for SQL execution
        # ✅ Insert query with parameter binding (safe against SQL injection)
        cursor.execute(
            """
                INSERT INTO doctor (id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            """, (id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id)  # ✅ values passed as tuple
        )
        conn.commit()  # ✅ Commit transaction so the new Doctors is saved
        print("[✓] Doctor Added Successfully.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()  # ❌ Rollback if something goes wrong
        print(f"[X] Error Inserting A New Doctor. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always clean up resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# DELETE
# -------------------


def delete_doc(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()       # ✅ Establish DB connection
        cursor = conn.cursor()        # ✅ Create cursor for executing SQL commands
        # ✅ Execute delete query safely using parameter binding (%s)
        cursor.execute(
            """
                DELETE FROM doctor WHERE id = %s
            """, (id,)   # tuple required (id,)
        )
        conn.commit()   # ✅ Save changes permanently
        print(f"[✓] Doctor with id {id} deleted.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()   # ❌ Undo changes if an error occurs (safety)
        print(f"[X] Error Deleting Doctor with id: '{id}'. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always release resources
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# Update
# -------------------


# Individual update functions for each doctor attribute
def update_doctor_fname(doctor_id, new_fname):
    # Calls helper function to update only the "first_name" field
    update_field(doctor_id, "first_name", new_fname)

def update_doctor_lname(doctor_id, new_lname):
    # Calls helper function to update only the "last_name" field
    update_field(doctor_id, "last_name", new_lname)

def update_doctor_gender(doctor_id, new_gender):
    # Calls helper function to update only the "gender" field
    update_field(doctor_id, "gender", new_gender)

def update_doctor_specialization(doctor_id, new_specialization):
    # Calls helper function to update only the "specialization" field
    update_field(doctor_id, "specialization", new_specialization)

def update_doctor_experience(doctor_id, new_experience):
    # Calls helper function to update only the "experience" field
    update_field(doctor_id, "experience", new_experience)

def update_doctor_contact(doctor_id, new_contact):
    # Calls helper function to update only the "contact" field
    update_field(doctor_id, "contact", new_contact)

def update_doctor_email(doctor_id, new_email):
    # Calls helper function to update only the "email" field
    update_field(doctor_id, "email", new_email)

def update_doctor_fee(doctor_id, new_fee):
    # Calls helper function to update only the "email" field
    update_field(doctor_id, "consultation_fee", new_fee)

def update_doctor_dept_id(doctor_id, new_dept_id):
    # Calls helper function to update only the "email" field
    update_field(doctor_id, "dept_id", new_dept_id)

# ✅ Generic helper function to update any allowed field
def update_field(doctor_id, field, value):
    # Define which fields are allowed to be updated (safety check)
    allowed_fields = {"first_name", "last_name", "gender", "specialization", "experience", "contact", "email", "consultation_fee", "dept_id"}
    if field not in allowed_fields:
        raise ValueError("Invalid Field Name")  # Prevents SQL injection
    conn = None
    cursor = None
    try:
        conn = get_connection()   # Open DB connection
        cursor = conn.cursor()
        # ⚠️ Using f-string for column name is okay here since it's validated
        # But values (field value + doctor_id) must use parameter binding (%s)
        query = f"UPDATE doctor SET {field} = %s WHERE id = %s"
        cursor.execute(query, (value, doctor_id))  # Safe against SQL injection
        conn.commit()  # Save changes
        print(f"[✓] Updated {field} for doctor {doctor_id}")
        return True
    except Exception as e:
        if conn:
            conn.rollback()  # Rollback in case of error (data integrity)
        print(f"[X] Error updating {field} for doctor {doctor_id}: {e}")
        return False
    finally:
        # Always close cursor & connection to avoid leaks
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# View One Doctor
# -------------------


def view_doc(doc_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                select id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id
                from doctor
                where id = %s
            """, (doc_id,)
        )
        result = cursor.fetchone()
        if result is None:
            return None  # No doctor found with given ID
        # ✅ Unpack tuple directly into variables
        id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id = result
        # ✅ Construct a clean dictionary for returning data
        doc_details = {
            "id" : id,
            "first_name" : first_name,
            "last_name" : last_name,
            "gender" : gender,
            "dob" : DOB,
            "specialization" : specialization,
            "experience" : experience,
            "contact" : contact,
            "email" : email,
            "consultation_fee" : consultation_fee,
            "dept_id": dept_id
        }
        return doc_details
    except Exception as e:
        # ❌ If something goes wrong, log error and return None (safe fallback)
        if conn:
            print(f"[X] Error Fetching Info For Doctor {doc_id}: {e}")
        return {} # Return empty dictionary instead of None for consistency
    finally:
# ✅ Ensure resources are always closed (important for production)
        if cursor: cursor.close()
        if conn: conn.close()

    
# -------------------
# View All Doctors
# -------------------


def view_all_doctors(limit = 100, offset = 0):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all doctors (id, first_name, last_name, gender, DOB, specialization, experience, contact, email)
        cursor.execute(
            """
                SELECT id, first_name, last_name, gender, DOB, specialization, experience, contact, email,consultation_fee, dept_id
                FROM doctor
                ORDER BY id LIMIT %s OFFSET %s
            """,(limit,offset)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "id" : id,
            "first_name" : first_name,
            "last_name" : last_name,
            "gender" : gender,
            "dob" : DOB,
            "specialization" : specialization,
            "experience" : experience,
            "contact" : contact,
            "email" : email,
            "consultation_fee" : consultation_fee,
            "dept_id": dept_id
            }
            for id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id in rows
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

def view_all_doctors_by_department(dept_id, limit = 100, offset = 0):
    conn = None
    cursor = None
    try:
        # ✅ Establish DB connection
        conn = get_connection()
        cursor = conn.cursor()
        # ✅ Fetch all doctors (id, first_name, last_name, gender, DOB, specialization, experience, contact, email)
        cursor.execute(
            """
                SELECT id, first_name, last_name, gender, DOB, specialization, experience, contact, email,consultation_fee, dept_id
                FROM doctor
                WHERE dept_id = %s
                ORDER BY id LIMIT %s OFFSET %s
            """,(dept_id, limit, offset)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "id" : id,
            "first_name" : first_name,
            "last_name" : last_name,
            "gender" : gender,
            "dob" : DOB,
            "specialization" : specialization,
            "experience" : experience,
            "contact" : contact,
            "email" : email,
            "consultation_fee" : consultation_fee,
            "dept_id": dept_id
            }
            for id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id in rows
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
# Count Doctors
# -------------------


def count_doctors():
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Execute COUNT query to get total number of doctors
        cursor.execute("SELECT COUNT(*) FROM doctor")
        # ✅ Fetch result (always returns a single row with one value)
        return cursor.fetchone()[0]
    except Exception as e:
        # ❌ If something goes wrong, log the error but don’t crash program
        if conn:
            print(f"[X] Error Counting Doctors: {e}")
        return None  # ✅ Safe fallback in case of error
    finally:
        # ✅ Ensure resources are always closed to prevent memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def count_doctors_by_specialization():
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Count doctors grouped by specialization
        cursor.execute(
                """
                    SELECT specialization, COUNT(*) as Total
                    FROM doctor
                    GROUP BY specialization
                    ORDER BY COUNT(*) DESC
 
                """
            )
        # ✅ Fetch all rows (list of tuples: [specialization, count] )
        results = cursor.fetchall() 
        # ✅ Convert to dict: {"Orthology": 12, "Gynacologist": 7 }
        return {row[0]: row[1] for row in results} if results else {} # ✅ Safe fallback if no rows
    except Exception as e:
        # ❌ If something goes wrong, log the error but don’t crash program
        if conn:
            print(f"[X] Error Counting Doctors By Specialization: {e}")
        return 0  # ✅ Safe fallback in case of error
    finally:
        # ✅ Ensure resources are always closed to prevent memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def count_doctors_by_gender():
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Count doctors grouped by gender
        cursor.execute(
                """
                    SELECT gender, COUNT(*) as Total
                    FROM doctor
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
            print(f"[X] Error Counting Doctors By Gender: {e}")
        return 0  # ✅ Safe fallback in case of error
    finally:
        # ✅ Ensure resources are always closed to prevent memory leaks
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# Check Existence Of Doctor
# -------------------


def doctor_exists_contact(contact):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any doctor exists with the given contact
        cursor.execute("SELECT id FROM doctor WHERE contact = %s LIMIT 1", (contact,))
        return cursor.fetchone() is not None # ✅ True if exists, False if not
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Doctor: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def doctor_exists_id(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any patient exists with the given contact
        cursor.execute("SELECT id FROM doctor WHERE id = %s", (id,))
        # ✅ fetchone() returns a row if found, otherwise None
        print(f"Doctor Exists With Id: {id}")
        return cursor.fetchone() is not None
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Doctor: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()


# -------------------
# Search Doctors
# -------------------


def search_doc_by_contact(contact):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Fetch the Doctor details by contact using parameter binding (%s)
        cursor.execute(
            """
                SELECT id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id
                FROM doctor
                WHERE contact = %s
            """, (contact,)   # tuple required: (contact,)
        )
        result = cursor.fetchone()   # ✅ Returns single row or None
        if result is None:
            return None  # No Doctor found with given ID
        # ✅ Unpack tuple directly into variables
        id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id = result 
        # ✅ Construct a clean dictionary for returning data
        doc_details = {
            "id" : id,
            "first_name" : first_name,
            "last_name" : last_name,
            "gender" : gender,
            "dob" : DOB,
            "specialization" : specialization,
            "experience" : experience,
            "contact" : contact,
            "email" : email,
            "consultation_fee" : consultation_fee,
            "dept_id" : dept_id
        }
        return doc_details
    except Exception as e:
        # ❌ If something goes wrong, log error and return None (safe fallback)
        if conn:
            print(f"[X] Error Fetching Info For Doctor With Contact Number {contact}: {e}")
        return {} # Return empty dictionary instead of None for consistency
    finally:
        # ✅ Ensure resources are always closed (important for production)
        if cursor: cursor.close()
        if conn: conn.close()

def search_doc_by_fname_lname(fname, lname):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                select id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id
                from doctor
                where first_name = %s AND last_name = %s
            """, (fname, lname)
        )
        result = cursor.fetchone()
        if result is None:
            return None  # No doctor found with given ID
        # ✅ Unpack tuple directly into variables
        id, first_name, last_name, gender, DOB, specialization, experience, contact, email, consultation_fee, dept_id = result
        # ✅ Construct a clean dictionary for returning data
        doc_details = {
            "id" : id,
            "first_name" : first_name,
            "last_name" : last_name,
            "gender" : gender,
            "dob" : DOB,
            "specialization" : specialization,
            "experience" : experience,
            "contact" : contact,
            "email" : email,
            "consultation_fee" : consultation_fee,
            "dept_id" : dept_id
        }
        return doc_details
    except Exception as e:
        # ❌ If something goes wrong, log error and return None (safe fallback)
        if conn:
            print(f"[X] Error Fetching Info For Doctor {fname} {lname}: {e}")
        return {} # Return empty dictionary instead of None for consistency
    finally:
# ✅ Ensure resources are always closed (important for production)
        if cursor: cursor.close()
        if conn: conn.close()

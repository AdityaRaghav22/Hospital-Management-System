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

def insert_dept(id, name, description):
    conn = None
    cursor = None
    try:
        conn = get_connection()        # ✅ Establish DB connection
        cursor = conn.cursor()         # ✅ Create cursor for SQL execution
        # ✅ Insert query with parameter binding (safe against SQL injection)
        cursor.execute(
            """
                INSERT INTO department (id, name, description)
                VALUES (%s, %s, %s)
            """, (id, name, description)  # ✅ values passed as tuple
        )
        conn.commit()  # ✅ Commit transaction so the new department is saved
        print("[✓] Department created Successfully.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()  # ❌ Rollback if something goes wrong
        print(f"[X] Error creating A New Department. Try Again Later \n error: {e}")
        return False
    finally:
        # ✅ Always clean up resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def delete_department(dept_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()        # ✅ Establish DB connection
        cursor = conn.cursor()         # ✅ Create cursor for SQL execution
        # ✅ Insert query with parameter binding (safe against SQL injection)
        cursor.execute(
            """
                DELETE FROM department WHERE id = %s
            """,(dept_id,)   # tuple required (id,)
        )
        conn.commit()   # ✅ Save changes permanently
        print(f"[✓] Department with id {dept_id} deleted.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()   # ❌ Undo changes if an error occurs (safety)
        print(f"[X] Error Deleting Department With ID: '{dept_id}'. Try Again Later \n Error: {e}")
        return False
    finally:
        # ✅ Always release resources
        if cursor: cursor.close()
        if conn: conn.close()

def update_department(dept_id, name=None, description= None):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Dynamically build update query
        updates = []
        values = []
        if name:
            updates.append("name = %s")
            values.append(name)
        if description:
            updates.append("description = %s")
            values.append(description)
        if not updates:
            print("[!] No fields to update.")
            return False
        query = f"""
            UPDATE department
            SET {', '.join(updates)}
            WHERE id = %s
        """
        values.append(dept_id)
        cursor.execute(query, values)
        conn.commit()
        print(f"[✓] Department with ID {dept_id} updated successfully.")
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[X] Error updating Department with ID {dept_id}: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_department(dept_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Fetch the department details by ID using parameter binding (%s)
        cursor.execute(
            """
                
                SELECT id, name, description
                FROM department
                WHERE id = %s
            """, (dept_id,)   # tuple required: (dept_id,)
        )
        row = cursor.fetchone()
        # ✅ Convert rows into a list of dicts for readability
        if not row:
            return {}
        return {
            "department_id": row[0],
            "department_name": row[1],
            "department_description": row[2]
        }
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Department Info With ID: '{dept_id}'. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_all_departments(limit=100, offset=0):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor for running SQL queries
        # ✅ Fetch the department details by ID using parameter binding (%s)
        cursor.execute(
            """
                
                SELECT id, name, description
                FROM department
                LIMIT %s OFFSET %s
            """(limit,offset)
        )
        rows = cursor.fetchall()
        # ✅ Convert rows into a list of dicts for readability
        return [
            {
            "department_id": department_id,
            "department_name": department_name,
            "department_description": department_description
            }
            for department_id, department_name, department_description in rows
        ]
    except Exception as e:
        # ✅ Log errors but don’t crash the program
        if conn:
            print(f"[X] Error Fetching Department Info. Try Again Later \n Error: {e}")
        return []  #  Return empty list instead of None for consistency
    finally:
        # ✅ Always close resources (best practice in DB code)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def department_exists(name):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any department exists with the given contact
        cursor.execute("""
                            SELECT id 
                            FROM department
                            WHERE name = %s
                       """, (name,))
        # ✅ fetchone() returns a row if found, otherwise None
        row = cursor.fetchone()
        if row:
            print(f"Department Exists With Name: {name}")
            return True
        else:
            print(f"No Department Found For Name: {name}")
            return False
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Department: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

def department_exists_id(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()   # ✅ Establish DB connection
        cursor = conn.cursor()    # ✅ Create cursor to run SQL queries
        # ✅ Check if any department exists with the given contact
        cursor.execute("""
                            SELECT id 
                            FROM department
                            WHERE id = %s
                       """, (id,))
        # ✅ fetchone() returns a row if found, otherwise None
        row = cursor.fetchone()
        if row:
            print(f"Department Exists With Id: {id}")
            return True
        else:
            print(f"No Department Found For Id: {id}")
            return False
    except Exception as e:
        # ❌ Log error but don’t stop the entire program
        if conn:
            print(f"[X] Error Checking Department: {e}")
        return False  # ✅ Safe fallback in case of error
    finally:
        # ✅ Always close resources to avoid memory leaks
        if cursor: cursor.close()
        if conn: conn.close()

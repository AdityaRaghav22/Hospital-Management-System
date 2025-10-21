import database.db_doc as doc
import backend.utils as util
from datetime import datetime

def add_doc(fname, lname, gender, dob, specialization, experience, contact, email, consultation_fee, dept_id):
    fname = fname.title().strip()
    lname = lname.title().strip()
    
    valid_gender = ["Male", "Female", "Prefer Not To Say"]
    if gender not in valid_gender:
        print(f"[X] Invalid Gender: {gender}")
        return False
    
    try:
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
        print("Valid Date Given")
    except Exception as e:
        print(f"Valid Date Not Given: {dob}. Try Again Later \n error: {e}")
        return False
    
    specialization = specialization.title().strip()

    if not str(experience).isdigit():
            print(f"Enter Valid Experience ")
            return False
    
    if not str(contact).isdigit():
            print(f"Enter Valid Contact Number ")
            return False
    
    if doc.doctor_exists_contact(contact):
        print("Doctor Exists Alread")
        return False
    
    if not util.valid_email(email):
        print(f"Enter Valid Email ")
        return False
    
    if not str(consultation_fee).isdigit():
        print(f"Enter Valid Consultation Fee")
        return False
    
    if not (isinstance(dept_id, str) and dept_id.upper().startswith("DEP") and dept_id.isalnum()):
        print(f"Enter Valid Department Id")
        return False
    
    try:
        doctor_id = util.generate_id("doctor")
        experience = int(experience)
        contact = int(contact)
        consultation_fee = int(consultation_fee)
        doc.insert_doc(doctor_id, fname, lname, gender, dob, specialization, experience, contact, email, consultation_fee, dept_id)
        print(f"Doctor Successfully Added: {fname} {lname}")
        return True
    except Exception as e:
        print(f"[X] Failed To Add Doctor: {fname} {lname}. Error: {e}")
        return False
    
def delete_doctor(doc_id):
    if not util.validate_id(doc_id, "DOCT"):
        print("Enter Valid Doctor Id")
        return False

    if doc.doctor_exists_id(doc_id):
        try:
            doc.delete_doc(doc_id)
            print(f"Doctor Successfully Deleted: {doc_id}")
            return True
        except Exception as e:
            print(f"[X] Failed To Delete Doctor: {doc_id}. Error: {e}")
            return False
    else:
        print(f"[X] Doctor Don't Exists With Id: {doc_id}")
        return False

def update_doctor(doc_id, fname = None, lname = None, gender = None, specialization = None, experience = None, contact = None, email = None, fee = None, dept_id = None):
    valid_gender = ["Male", "Female", "Prefer Not To Say"]
    if not util.validate_id(doc_id, "DOCT"):
        print("Enter Valid Doctor Id")
        return False

    if doc.doctor_exists_id(doc_id):
        try:
            if fname:
                fname = fname.title().strip()
                doc.update_doctor_fname(doc_id, fname)
                print(f"Doctor's First Name Successfully Updated: {fname}")

            if lname:
                lname = lname.title().strip()
                doc.update_doctor_lname(doc_id, lname)
                print(f"Doctor's Last Name Successfully Updated: {lname}")

            if gender:
                gender = gender.title().strip()
                if gender not in valid_gender:
                    print(f"[X] Invalid Gender: {gender}")
                    return False
                
                doc.update_doctor_gender(doc_id, gender)
                print(f"Doctor's Gender Successfully Updated: {gender}")

            if specialization:
                specialization = specialization.title().strip()
                doc.update_doctor_specialization(doc_id, specialization)
                print(f"Doctor's Specialization Successfully Updated: {specialization}")

            if experience:
                if not str(experience).isdigit():
                    print(f"Enter Valid Experience ")
                    return False
                
                experience = int(experience)
                doc.update_doctor_experience(doc_id, experience)
                print(f"Doctor's Experience Successfully Updated: {experience}")

            if contact:
                if not str(contact).isdigit():
                    print(f"Enter Valid Contact Number ")
                    return False
                
                doc.update_doctor_contact(doc_id, contact)
                print(f"Doctor's Contact Successfully Updated: {contact}")

            if email:
                if not util.valid_email(email):
                    print(f"Enter Valid Email ")
                    return False
                
                doc.update_doctor_email(doc_id, email)
                print(f"Doctor's Email Successfully Updated: {email}")

            if fee:
                if not str(fee).isdigit():
                    print(f"Enter Valid Consultation Fee")
                    return False
                
                doc.update_doctor_fee(doc_id, fee)
                print(f"Doctor's Consulting Fee Successfully Updated: {fee}")

            if dept_id:

                if not util.validate_id(dept_id,"DEPT"):
                    print(f"Enter Valid Department Id")
                    return False

                doc.update_doctor_dept_id(doc_id, dept_id)
                print(f"Doctor's Department Id Successfully Updated: {dept_id}")

            return True
        
        except Exception as e:
            print(f"[X] Failed To Update Doctor With Id: {doc_id}. Error: {e}")
            return False
        
    else:
        print(f"[X] Doctor Don't Exists With Id: {doc_id}")
        return False
    
def view_one_doc(doc_id):
    if not util.validate_id(doc_id, "DOCT"):
        print("Enter Valid Doctor Id")
        return False

    if doc.doctor_exists_id(doc_id):
        try:
            doc_details = doc.view_doc(doc_id)
            result = {
                "id" : doc_details["id"],
                "first_name" : doc_details["first_name"],
                "last_name" : doc_details["last_name"],
                "gender" : doc_details["gender"],
                "dob" : doc_details["DOB"],
                "specialization" : doc_details["specialization"],
                "experience" : doc_details["experience"],
                "contact" : doc_details["contact"],
                "email" : doc_details["email"],
                "consultation_fee" : doc_details["consultation_fee"],
                "dept_id": doc_details["dept_id"]
            }
            print(f"Doctor's Details Successfully Fetched With Id: {doc_id}")
            return True, result
        except Exception as e:
            print(f"[X] Failed To Fetch Doctor's Details With Id: {doc_id}. Error: {e}")
            return False, {}
    else:
        print(f"[X] Doctor Don't Exists With Id: {doc_id}")
        return False, {}
    
def view_all_doctors():
    try:
        doc_list = doc.view_all_doctors()
        result = {
            "doctors": doc_list
        }
        print(f"[✓] Fetched {len(doc_list)} Doctors Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Doctors. Error: {e}")
        return False, {"doctors": []}

def view_doctor_by_dept(dept_id):
    if not util.validate_id(dept_id, "DEPT"):
        print("Enter Valid Department Id")
        return False
    try:
        doc_list = doc.view_all_doctors_by_department(dept_id)
        result = {
            "doctors": doc_list
        }
        print(f"[✓] Fetched {len(doc_list)} Doctor Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Doctor. Error: {e}")
        return False, {"doctors": []}
    
def search_doctor_by_contact(contact):
    if not str(contact).isdigit():
        print(f"Enter Valid Contact Number ")
        return False
    contact = int(contact)
    try:
            doc_details = doc.search_doc_by_contact(contact)
            result = {
                "id" : doc_details["id"],
                "first_name" : doc_details["first_name"],
                "last_name" : doc_details["last_name"],
                "gender" : doc_details["gender"],
                "dob" : doc_details["DOB"],
                "specialization" : doc_details["specialization"],
                "experience" : doc_details["experience"],
                "contact" : doc_details["contact"],
                "email" : doc_details["email"],
                "consultation_fee" : doc_details["consultation_fee"],
                "dept_id": doc_details["dept_id"]
            }
            print(f"Doctor's Details Successfully Fetched With Contact: {contact}")
            return True, result
    except Exception as e:
            print(f"[X] Doctor Don't Exists Or Failed To Fetch Doctor's Details With Contact: {contact}. Error: {e}")
            return False, {}
    
def search_doctor_by_names(fname, lname):
    fname = fname.title().strip()
    lname = lname.title().strip()
    try:
            doc_details = doc.search_doc_by_fname_lname(fname, lname)
            result = {
                "id" : doc_details["id"],
                "first_name" : doc_details["first_name"],
                "last_name" : doc_details["last_name"],
                "gender" : doc_details["gender"],
                "dob" : doc_details["DOB"],
                "specialization" : doc_details["specialization"],
                "experience" : doc_details["experience"],
                "contact" : doc_details["contact"],
                "email" : doc_details["email"],
                "consultation_fee" : doc_details["consultation_fee"],
                "dept_id": doc_details["dept_id"]
            }
            print(f"Doctor's Details Successfully Fetched With Name: {fname} {lname}")
            return True, result
    except Exception as e:
            print(f"[X] Doctor Don't Exists Or Failed To Fetch Doctor's Details With Name: {fname} {lname}. Error: {e}")
            return False, {}

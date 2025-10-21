import database.db_patients as pt
import backend.utils as util

def add_patient(name, gender, age, blood_grp, contact):
    name = name.title().strip()
    gender = gender.title().strip()
    valid_gender = ["Male", "Female", "Prefer Not To Say"]

    if gender not in valid_gender:
        print(f"[X] Invalid Gender: {gender}")
        return False
    
    blood_grp = blood_grp.upper().strip()
    valid_bg = [ "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-" ]

    if not str(contact).isdigit():
            print(f"Enter Valid Contact Number ")
            return False
    
    if pt.patient_exists_contact(contact):
        print("Patient Exists Already")
        return False
    
    if not str(age).isdigit():
            print(f"Enter Valid Age")
            return False
    
    if blood_grp not in valid_bg:
        print(f"[X] Invalid Blood Group: {blood_grp}")
        return False
    
    try:
        patient_id = util.generate_id("patient")
        age = int(age)
        contact = int(contact)
        pt.insert_patient(patient_id, name,gender,age,blood_grp,contact)
        print(f"Patient Successfully Added: {name}")
        return True
    
    except Exception as e:
        print(f"[X] Failed To Add Patient: {name}. Error: {e}")
        return False

def delete_patient(patient_id):
    
    if not util.validate_id(patient_id, "PATI"):
        print("Enter Valid Patient ID")
        return False

    if pt.patient_exists_id(patient_id):
        try:
            pt.delete_patients(patient_id)
            print(f"Patient Successfully Deleted: {patient_id}")
            return True
        except Exception as e:
            print(f"[X] Failed To Delete Patient: {patient_id}. Error: {e}")
            return False
    else:
        print(f"[X] Patient Don't Exists With Id: {patient_id}")
        return False
    
def update_patient_details(patient_id, name = None, gender = None, age = None, contact = None, blood_grp = None):

    if not util.validate_id(patient_id, "PATI"):
        print("Enter Valid Patient ID")
        return False

    valid_gender = ["Male", "Female", "Prefer Not To Say"]
    valid_bg = [ "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-" ]
    if pt.patient_exists_id(patient_id):
        try:
            if name:
                name = name.title().strip()
                pt.update_patient_name(patient_id,name)
                print(f"Patient's Name Successfully Updated: {name}")
            if gender:
                gender = gender.title().strip()
                if gender not in valid_gender:
                    print(f"[X] Invalid Gender: {gender}")
                    return False
                pt.update_patient_gender(patient_id,gender)
                print(f"Patient's Gender Successfully Updated: {gender}")
            if age:
                if not str(age).isdigit():
                    print(f"Enter Valid Age")
                    return False
                age = int(age)
                pt.update_patient_age(patient_id, age)
                print(f"Patient's Age Successfully Updated: {age}")
            if contact:
                if not str(contact).isdigit():
                    print(f"Enter Valid Contact Number ")
                    return False
                contact = int(contact)
                pt.update_patient_contact(patient_id, contact)
                print(f"Patient's Contact Successfully Updated: {contact}")
            if blood_grp:
                blood_grp = blood_grp.upper().strip()
                if blood_grp not in valid_bg:
                    print(f"[X] Invalid Blood Group: {blood_grp}")
                    return False
                pt.update_patient_blood_group(patient_id, blood_grp)
                print(f"Patient's Blood Group Successfully Updated: {blood_grp}")
            return True
        except Exception as e:
            print(f"[X] Failed To Update Patient With Id: {patient_id}. Error: {e}")
            return False
    else:
        print(f"[X] Patient Don't Exists With Id: {patient_id}")
        return False
    
def view_one_patient(patient_id):
    if not util.validate_id(patient_id, "PATI"):
        print("Enter Valid Patient ID")
        return False
    
    if pt.patient_exists_id(patient_id):
        try:
            patient_details= pt.view_patient(patient_id)
            result = {
                "id" : patient_details["id"],
                "name" : patient_details["name"],
                "gender" : patient_details["gender"],
                "age" : patient_details["age"],
                "blood_group" : patient_details["blood_group"],
                "contact" : patient_details["contact"]
            }
            print(f"Patient's Details Successfully Fetched With Id: {patient_id}")
            return True, result
        except Exception as e:
            print(f"[X] Failed To Fetch Patient's Details With Id: {patient_id}. Error: {e}")
            return False, {}
    else:
        print(f"[X] Patient Don't Exists With Id: {patient_id}")
        return False, {}
    
def view_all_patient():
    try:
        patients_list = pt.view_all_patients()
        result = {
            "patients": patients_list
        }
        print(f"[✓] Fetched {len(patients_list)} Patients Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Patients. Error: {e}")
        return False, {"patients": []}

def search_patient_contact(contact):
    if not str(contact).isdigit():
        print(f"Enter Valid Contact Number ")
        return False
    contact = int(contact)
    if pt.patient_exists_contact(contact):
        try:
            patient_details= pt.search_patient_by_contact(contact)
            result = {
                "id" : patient_details["id"],
                "name" : patient_details["name"],
                "gender" : patient_details["gender"],
                "age" : patient_details["age"],
                "blood_group" : patient_details["blood_group"],
                "contact" : patient_details["contact"]
            }
            print(f"Patient's Details Successfully Fetched With Contact: {contact}")
            return True, result
        except Exception as e:
            print(f"[X] Failed To Fetch Patient's Details With Contact: {contact}. Error: {e}")
            return False, {}
    else:
        print(f"[X] Patient Don't Exists With Contact: {contact}")      
        return False, {}
    
def search_patient_by_blood_group(blood_group):
    blood_group = blood_group.upper().strip()
    valid_bg = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if blood_group not in valid_bg:
        print(f"[X] Invalid Blood Group: {blood_group}")
        return False, {"patients": []}
    try:
        patients_list = pt.search_by_blood_group(blood_group)
        result = {
            "patients": patients_list
        }
        print(f"[✓] Fetched {len(patients_list)} Patients Successfully With Blood Group: {blood_group}")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Patients With Blood Group: {blood_group}. Error: {e}")
        return False, {"patients": []}

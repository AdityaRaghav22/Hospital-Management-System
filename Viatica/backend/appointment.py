import database.db_appointment as ap
import backend.utils as util
from datetime import datetime


def add_appointment(patient_id, doc_id, date, time, reason, status = "Scheduled"):

    valid_status = ["Scheduled", "Completed", "Cancelled"]
    
    if not util.validate_id(patient_id,"PATI"):
        print(f"Enter Valid Patient Id")
        return False
    
    if not util.validate_id(doc_id,"DOCT"):
        print(f"Enter Valid Doctor Id")
        return False
    
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        date = date_obj.strftime("%d/%m/%Y")
        print("Valid Date Given")
    except Exception as e:
        print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
        return False
    
    try:
        time_obj = datetime.strptime(time, "%H:%M")
        time = time_obj.strftime("%H:%M")
        print("Valid Time Given")
    except ValueError:
        return False
    
    reason = reason.title().strip()

    status = status.title().strip()

    if status not in valid_status:
        print(f"[X] Invalid Status: {status}")
        return False    
    
    try:
        appointment_id = util.generate_id("appointment")
    
        if ap.appointment_exists_patient_id(patient_id, date, time):
            print("Appointment Already Exists")
            return False
        
        ap.insert_appointment(appointment_id, patient_id, doc_id, date, time, reason, status)

    except Exception as e:
        print(f"[X] Failed To Add Appointment With Patient Id: {patient_id}, Doctor's Id: {doc_id}. Error: {e}")
        return False

def delete_appointment(appointment_id):

    if not util.validate_id(appointment_id, "APPO"):
        print("Enter Valid Doctor Id")
        return False

    if ap.appointment_exists(appointment_id):
        try:
            ap.delete_appointment(appointment_id)
            print(f"Appointment Successfully Deleted: {appointment_id}")
            return True
        
        except Exception as e:
            print(f"[X] Failed To Delete Appointment: {appointment_id}. Error: {e}")
            return False
        
    else:
        print(f"[X] Appointment Don't Exists With Id: {appointment_id}")
        return False

def update_appointment(appointment_id, date = None, time = None, reason = None, doc_id = None, status = None):

    valid_status = ["Scheduled", "Completed", "Cancelled"]

    if not util.validate_id(appointment_id, "APPO"):
        print("Enter Valid Doctor Id")
        return False

    if ap.appointment_exists_id(appointment_id):
        try:
            if date:
                try:
                    date_obj = datetime.strptime(date, "%d/%m/%Y").date()
                    date = date_obj.strftime("%d/%m/%Y")
                    print("Valid Date Given")

                except Exception as e:
                    print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
                    return False
                
                ap.update_appointment_date(appointment_id, date)

            if time:
                try:
                    time_obj = datetime.strptime(time, "%H:%M")
                    time = time_obj.strftime("%H:%M")
                    print("Valid Time Given")

                except ValueError:
                    return False
                
                ap.update_appointment_time(appointment_id, time)

            if reason:
                reason = reason.title().strip()

                ap.update_appointment_reason(appointment_id,reason)

            if doc_id:
                if not util.validate_id(doc_id, "DOCT"):
                    print(f"Enter Valid Doctor Id")
                    return False
                
                doc_id = int(doc_id)

                ap.update_appointment_doc_id(appointment_id, doc_id)

            if status:
                status = status.title().strip()

                if status not in valid_status:
                    print(f"[X] Invalid Status: {status}")
                    return False
                
                ap.update_appointment_status(appointment_id, status)

            return True
        
        except Exception as e:
            print(f"[X] Failed To Update Appointment With Id: {appointment_id}. Error: {e}")
            return False
        
    else:
        print(f"[X] Appointment Don't Exists With Id: {appointment_id}")
        return False
    
def view_one_appointment(appointment_id):
    if not util.validate_id(appointment_id, "APPO"):
        print("Enter Valid Doctor Id")
        return False
    if ap.appointment_exists_id(appointment_id):
        try:
            appointment_details = ap.view_patient_appointment(appointment_id)
            result = {
                "appointment_id" : appointment_details["appointment_id"],
                "patient_name" : appointment_details["patient_name"],
                "patient_age" : appointment_details["patient_age"],
                "doctor_name" : appointment_details["doctor_name"],
                "doctor_specialization" : appointment_details["doctor_specialization"],
                "appointment_date" : appointment_details["appointment_date"],
                "appointment_time" : appointment_details["appointment_time"],
                "reason" : appointment_details["reason"],
                "status": appointment_details["status"]
            }
            print(f"Appointment Details Successfully Fetched With Id: {appointment_id}")
            return True, result
        except Exception as e:
            print(f"[X] Failed To Fetch Appointment Details With Id: {appointment_id}. Error: {e}")
            return False, {}
    else:
        print(f"[X] Appointment Doesn't Exists With Id: {appointment_id}")
        return False, {}

def view_appointments_for_patient(patient_id):
    try:
        if not util.validate_id(patient_id, "PATI"):
            print("Enter Valid Doctor Id")
            return False
    
        appointment_list = ap.view_patient_appointments(patient_id)
        result = {
            "appointments": appointment_list
        }
        print(f"[✓] Fetched {len(appointment_list)} Appointments Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Appointments. Error: {e}")
        return False, {"appointments": []}
    
def view_appointments_for_doctor(doc_id):
    try:
        if not util.validate_id(doc_id, "DOCT"):
            print("Enter Valid Doctor Id")
            return False
        appointment_list = ap.view_doctor_appointments(doc_id)
        result = {
            "appointments": appointment_list
        }
        print(f"[✓] Fetched {len(appointment_list)} Appointments Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Appointments. Error: {e}")
        return False, {"appointments": []}
    
def view_all_appointments():
    try:
        appointments_list = ap.view_all_appointments()
        result = {
            "appointments": appointments_list
        }
        print(f"[✓] Fetched {len(appointments_list)} Appointments Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Appointments. Error: {e}")
        return False, {"appointments": []}

def view_all_appointments_by_date(date):
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        date = date_obj.strftime("%d/%m/%Y")
        print("Valid Date Given")
    except Exception as e:
        print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
        return False

    try:
        appointments_list = ap.search_appointment_by_date(date)
        result = {
            "appointments": appointments_list
        }
        print(f"[✓] Fetched {len(appointments_list)} Appointments Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Appointments. Error: {e}")
        return False, {"Appointments": []}

def view_all_appointments_by_status(status):
    valid_status = ["Scheduled", "Completed", "Cancelled"]
    status = status.title().strip()

    if status not in valid_status:
        print(f"[X] Invalid Status: {status}")
        return False

    try:
        appointments_list = ap.search_appointment_by_status(status)
        result = {
            "appointments": appointments_list
        }
        print(f"[✓] Fetched {len(appointments_list)} Appointments Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Appointments. Error: {e}")
        return False, {"Appointments": []}

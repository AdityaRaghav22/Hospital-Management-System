import database.db_doc_schedule as avail
import backend.utils as util
from datetime import datetime

def add_availability(doc_id, date, day, start, end, duration):
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if not (isinstance(doc_id, str) and doc_id.upper().startswith("PAT") and doc_id.isalnum()):
        print(f"Enter Valid Doctor Id")
        return False
        
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        date = date_obj.strftime("%d/%m/%Y")
        print("Valid Date Given")
    except Exception as e:
        print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
        return False
    
    if day not in valid_days:
        print(f"Enter Valid Day")
        return False

    try:
        start_time_obj = datetime.strptime(start, "%H:%M")
        start = start_time_obj.strftime("%H:%M")
        print("Valid Start Time Given")
    except ValueError:
        return False
    
    try:
        end_time_obj = datetime.strptime(end, "%H:%M")
        start = end_time_obj.strftime("%H:%M")
        print("Valid End Time Given")
    except ValueError:
        return False
    
    try:
        duration_obj = datetime.strptime(duration, "%M")
        start = duration_obj.strftime("%M")
        print("Valid End Time Given")
    except ValueError:
        return
    
    try:
        avail_id = util.generate_id("availability")

        if avail.availability_exists(avail_id):
            return False
        
        avail.add_availability(avail_id, doc_id, day, start, end, duration)
    except Exception as e:
        print(f"[X] Failed To Add Availability For Doctor's Id: {doc_id}. Error: {e}")
        return False

def delete_availability(availability_id):
    if not util.validate_id(availability_id, "AVA"):
        print("Enter Valid Slot Id")
        return False
    
    if avail.availability_exists(availability_id):
        try:
            avail.delete_slot(availability_id)
            print(f"Slot Successfully Deleted: {availability_id}")
            return True
        except Exception as e:
            print(f"[X] Failed To Delete Slot: {availability_id}. Error: {e}")
            return False
    else:
        print(f"[X] Slot Don't Exists With Id: {availability_id}")
        return False
    
def delete_slot_doc_id(doc_id, date, start_time = None):
    if not util.validate_id(doc_id, "DOC"):
        print("Enter Valid Doctor Id")
        return False
    
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        date = date_obj.strftime("%d/%m/%Y")
        print("Valid Date Given")
    except Exception as e:
        print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
        return False
    
    try:
        start_time_obj = datetime.strptime(start_time, "%H:%M")
        start_time = start_time_obj.strftime("%H:%M")
        print("Valid Start Time Given")
    except ValueError:
        return False
    
    if avail.availability_exists_doc(doc_id, date, start_time):
        try:
            avail.delete_slot_with_doc_id(doc_id, date, start_time)
            print(f"Slot Successfully Deleted: {doc_id}")
            return True
        except Exception as e:
            print(f"[X] Failed To Delete Slot: {doc_id}. Error: {e}")
            return False
    else:
        print(f"[X] Slot Don't Exists With Id: {doc_id}")
        return False
    
def update_slot_booked(avail_id, date, start_time):
    if not util.validate_id(avail_id, "AVA"):
        print("Enter Valid Doctor Id")
        return False
    
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        date = date_obj.strftime("%d/%m/%Y")
        print("Valid Date Given")
    except Exception as e:
        print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
        return False
    
    try:
        start_time_obj = datetime.strptime(start_time, "%H:%M")
        start_time = start_time_obj.strftime("%H:%M")
        print("Valid Start Time Given")
    except ValueError:
        return False
    
    if avail.availability_exists(avail_id):
        try:
            avail.mark_slot_booked(avail_id, date, start_time)
            print(f"Slot Successfully Booked: {avail_id}")
            return True
        except Exception as e:
            print(f"[X] Failed To Book Slot: {avail_id}. Error: {e}")
            return False
    else:
        print(f"[X] Slot Don't Exists With Id: {avail_id}")
        return False
    
def update_slot_free(avail_id, date, start_time):
    if not util.validate_id(avail_id, "AVA"):
        print("Enter Valid Doctor Id")
        return False
    
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        date = date_obj.strftime("%d/%m/%Y")
        print("Valid Date Given")
    except Exception as e:
        print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
        return False
    
    try:
        start_time_obj = datetime.strptime(start_time, "%H:%M")
        start_time = start_time_obj.strftime("%H:%M")
        print("Valid Start Time Given")
    except ValueError:
        return False
    
    if avail.availability_exists(avail_id):
        try:
            avail.mark_slot_free(avail_id, date, start_time)
            print(f"Slot Successfully Free: {avail_id}")
            return True
        except Exception as e:
            print(f"[X] Failed To Free Slot: {avail_id}. Error: {e}")
            return False
    else:
        print(f"[X] Slot Don't Exists With Id: {avail_id}")
        return False
    
def view_slot_for_doc(doc_id):
    try:
        if not util.validate_id(doc_id, "DOC"):
            print("Enter Valid Doctor Id")
            return False
        avail_list = avail.view_all_availability_for_doc(doc_id)
        result = {
            "availabilities": avail_list
        }
        print(f"[✓] Fetched {len(avail_list)} Availabilites Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Availabilites. Error: {e}")
        return False, {"availabilites": []}

def view_day_slots(doc_id, date):
    try:
        if not util.validate_id(doc_id, "DOC"):
            print("Enter Valid Doctor Id")
            return False
        
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y").date()
            date = date_obj.strftime("%d/%m/%Y")
            print("Valid Date Given")
        except Exception as e:
            print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
            return False

        avail_list = avail.view_day_schedule(doc_id, date)
        result = {
            "availabilities": avail_list
        }
        print(f"[✓] Fetched {len(avail_list)} Availabilites Successfully")
        return True, result
    
    except Exception as e:
        print(f"[X] Failed To Fetch Availabilites. Error: {e}")
        return False, {"availabilites": []}
    
def view_free_slots(doc_id, date):
    try:
        if not util.validate_id(doc_id, "DOC"):
            print("Enter Valid Doctor Id")
            return False
        
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y").date()
            date = date_obj.strftime("%d/%m/%Y")
            print("Valid Date Given")
        except Exception as e:
            print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
            return False

        avail_list = avail.view_free_slots(doc_id, date)
        result = {
            "availabilities": avail_list
        }
        print(f"[✓] Fetched {len(avail_list)} Availabilites Successfully")
        return True, result
    
    except Exception as e:
        print(f"[X] Failed To Fetch Availabilites. Error: {e}")
        return False, {"availabilites": []}
    
def view_booked_slots(doc_id, date):
    try:

        if not util.validate_id(doc_id, "DOC"):
            print("Enter Valid Doctor Id")
            return False
        
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y").date()
            date = date_obj.strftime("%d/%m/%Y")
            print("Valid Date Given")
        except Exception as e:
            print(f"Valid Date Not Given: {date}. Try Again Later \n error: {e}")
            return False

        avail_list = avail.view_booked_slots(doc_id, date)
        result = {
            "availabilities": avail_list
        }
        print(f"[✓] Fetched {len(avail_list)} Availabilites Successfully")
        return True, result
    
    except Exception as e:
        print(f"[X] Failed To Fetch Availabilites. Error: {e}")
        return False, {"availabilites": []}
    
def view_all_slots():
    try:
        avail_list = avail.view_all_availability()
        result = {
            "availabilities": avail_list
        }
        print(f"[✓] Fetched {len(avail_list)} Appointments Successfully")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Availability. Error: {e}")
        return False, {"availability": []}

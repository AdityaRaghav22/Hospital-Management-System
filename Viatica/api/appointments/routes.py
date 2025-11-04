from flask import Blueprint, request, jsonify
import backend.appointment as appo_logic
import backend.patient as pt
import backend.doctor as doc
import backend.qr as qr

appointment_bp = Blueprint("appointment", __name__, url_prefix="/appointment")

@appointment_bp.route("/add", methods = ["POST"])
def add_appointment():
    data = request.get_json()
    # required details
    contact = data.get("contact")
    doc_id = data.get("doc_id")
    date = data.get("date")
    time = data.get("time") 
    reason = data.get("reason")

    if not contact or not doc_id or not date or not time or not reason:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    try:    
        search_result, patient_details = pt.search_patient_contact(contact)
        if search_result:
            patient_id = patient_details["id"]
            print(f"Existing patient found: {patient_id}")
        else:
            print(f"New patient detected — adding...")
            name = data.get("name")          
            gender = data.get("gender")      
            age = data.get("age")            
            blood_grp = data.get("blood_grp")
            if not all([name, gender, age, blood_grp]):
                return jsonify({
                    "status": "error",
                    "message": "Patient not found — please provide name, gender, age, and blood group to register new patient."
                }), 400
            
            success = pt.add_patient(name, gender, age, blood_grp, contact)

            if not success:
                return jsonify({"status": "error", "message": "Failed to register new patient"}), 400
            
            patient_exists, patient_details = pt.search_patient_contact(contact)
            if not patient_exists:
                return jsonify({"status": "error", "message": "Patient registration failed"}), 400

            patient_id = patient_details["id"]
            print(f"New patient added: {patient_id}")

    except Exception as e:
        print(f"❌ Error handling patient: {e}")
        return jsonify({"status": "error", "message": "Internal error processing patient"}), 500
    
    try:
        search_result, doc_details = doc.view_one_doc(doc_id)
        if not search_result:
            return jsonify({"status": "error", "message": "Doctor not found"}), 404
        doc_id = doc_details["id"]

    except Exception as e:
        print(f"❌ Error fetching doctor: {e}")
        return jsonify({"status": "error", "message": "Internal error fetching doctor"}), 500   
    
    try:
        success = appo_logic.add_appointment(patient_id, doc_id, date, time, reason)
        qr.generating_qr(patient_id)
        if success:
            return jsonify({"status": "success", "message": "Appointment scheduled successfully"}), 201
        else:
            return jsonify({"status": "error", "message": "Failed to create appointment"}), 500
        
    except Exception as e:
        print(f"❌ Error adding appointment: {e}")
        return jsonify({"status": "error", "message": "Internal error creating appointment"}), 500
    

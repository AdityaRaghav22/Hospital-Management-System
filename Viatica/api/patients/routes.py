from flask import Blueprint, request, jsonify
import backend.patient as patient_logic

patients_bp = Blueprint("patients", __name__, url_prefix="/patients")

@patients_bp.route("/add", methods=["POST"])
def add_patient():
    data = request.get_json()
    name = data.get("name")
    gender = data.get("gender")
    age = data.get("age")
    blood_grp = data.get("blood_grp")
    contact = data.get("contact")

    success = patient_logic.add_patient(name, gender, age, blood_grp, contact)

    if success:
        return jsonify({"status": "success", "message": f"Patient {name} added successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Failed to add patient"}), 400

@patients_bp.route("/delete/<patient_id>", methods = ["DELETE"])
def delete_patient(patient_id):
    success = patient_logic.delete_patient(patient_id)
    if success:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Patient not found"}), 404

@patients_bp.route("/update/<patient_id>", methods = ["PUT"])
def update_patient(patient_id):
    data = request.get_json()
    success = patient_logic.update_patient_details(
        patient_id,
        name=data.get("name"),
        gender=data.get("gender"),
        age=data.get("age"),
        blood_grp=data.get("blood_grp"),
        contact=data.get("contact")
    )
    if success:
        return jsonify({"status": "success", "message": f"Patient {patient_id} updated successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to update patient"}), 400

@patients_bp.route("/<patient_id>", methods = ["GET"])
def get_patient(patient_id):
    success, result = patient_logic.view_one_patient(patient_id)
    if success:
        return jsonify({"status": "success", "patient": result}), 200
    else:
        return jsonify({"status": "error", "message": "Patient not found"}), 404
    
@patients_bp.route("/all", methods = ["GET"])
def get_all():
    success, result = patient_logic.view_all_patient()
    if success:
        return jsonify({"status": "success", "patients": result["patients"]}), 200
    else:
        return jsonify({"status": "error", "patients": []}), 400
    
@patients_bp.route("/contact/<contact>", methods = ["GET"])
def get_patient_by_contact(contact):
    success, result = patient_logic.search_patient_contact(contact)
    if success:
        return jsonify({"status": "success", "patient": result}), 200
    else:
        return jsonify({"status": "error", "message": "Patient not found"}), 404

@patients_bp.route("/bg/<blood_group>", methods = ["GET"])
def get_patient_by_blood_grp(blood_group):
    success, result = patient_logic.search_patient_by_blood_group(blood_group)
    if success:
        return jsonify({"status": "success", "patient": result}), 200
    else:
        return jsonify({"status": "error", "message": "Patient not found"}), 404

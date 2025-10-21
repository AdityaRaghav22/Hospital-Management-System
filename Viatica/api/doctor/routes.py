from flask import Blueprint, request, jsonify
import backend.doctor as doc_logic

doctors_bp = Blueprint("doctors", __name__, url_prefix="/doctors")

@doctors_bp.route("/add", methods = ["POST"])
def add_doc():
    data = request.get_json()
    fname = data.get("fname")
    lname = data.get("lname")
    gender = data.get("gender")
    dob = data.get("dob")
    specialization = data.get("specialization")
    experience = data.get("experience")
    contact = data.get("contact")
    email = data.get("email")
    consultation_fee = data.get("consultaion_fee")
    dept_id = data.get("dept_id")

    success = doc_logic.add_doc(fname, lname, gender, dob, specialization, experience, contact, email, consultation_fee, dept_id)

    if success:
        return jsonify({"status": "success", "message": f"Doctor {fname} added successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Failed to add doctor"}), 400
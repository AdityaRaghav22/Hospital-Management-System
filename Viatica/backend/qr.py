from database import db_qr as qr
import backend.patient as pt
import backend.utils as util


def generating_qr(patient_id):
    if not util.validate_id(patient_id, "PATI"):
        print("Enter Valid Patient ID")
        return False
    if qr.qr_exists(patient_id):
        success = qr.image_exists(patient_id)
        if success:
            print(f"✅ QR already exists for Patient {patient_id}")
            return False
        else:
            print(f"⚠️ QR record exists but image missing. Regenerating image...")
            qr.delete_qr(patient_id)    
            
    qr.create_patient_qr(patient_id)
    return True

def delete_qr(patient_id):
    pass
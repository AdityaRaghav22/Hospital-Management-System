from datetime import datetime
import random

def valid_email(email):
    pass

def generate_id(prefix):

    prefix = prefix.upper().strip()
    prefix = prefix[:4]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = random.randint(10, 99)

    return f"{prefix}{timestamp}{rand}"

def validate_id(entity_id, prefix):
    return isinstance(entity_id, str) and entity_id.upper().startswith(prefix) and entity_id.isalnum()

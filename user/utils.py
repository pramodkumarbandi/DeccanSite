import re

def validate_phone(phone):
    if not phone:
        return False, "Phone number is required"

    # Indian mobile number: starts with 6-9 and 10 digits
    if not re.fullmatch(r'[6-9]\d{9}', phone):
        return False, "Enter valid 10 digit mobile number"

    return True, "Valid phone number"

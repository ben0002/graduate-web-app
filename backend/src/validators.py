from pydantic import EmailStr
from datetime import datetime
import schemas

def validate_gender(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 40:
        raise ValueError("Invalid format. The Gender should be a string with at most 40 characters.")
    return value

def validate_firstname(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 40:
        raise ValueError("Invalid format. The First Name should be a string with at most 40 characters.")
    return value

def validate_lastname(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 40:
        raise ValueError("Invalid format. The Last Name should be a string with at most 40 characters.")
    return value

def validate_middlename(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 40:
        raise ValueError("Invalid format. The Middle Name should be a string with at most 40 characters.")
    return value

def validate_admitcamp(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 60:
        raise ValueError("Invalid format. The Address should be a string with at most 60 characters.")
    return value

def validate_degreename(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 30:
        raise ValueError("Invalid format. The Degree should be a string with at most 30 characters.")
    return value

def validate_majorname(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 30:
        raise ValueError("Invalid format. The Major Name should be a string with at most 30 characters.")
    return value

def validate_majordescription(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 500:
        raise ValueError("Invalid format. The Major Description should be a string with at most 500 characters.")
    return value

def validate_firstterm(value):
    if value is None:
        return value
    if not (isinstance(value, str) and value.isdigit() and len(value) == 6):
        raise ValueError("Invalid format. The First Term should be a 6-digit number yyyymm.")
    return value

def validate_date(value):
        if value is None:
            return value
        try:
            value = datetime.strptime(value, '%d-%b-%y').date()
        except ValueError:
            raise ValueError("Invalid date format. Should be in the format '31-MAR-22'.")
        return value
    
def validate_pos_chair(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 100:
        raise ValueError("Invalid format. The POS chair name should be a string with at most 100 characters.")
    return value

def validate_pos_co_chair(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 100:
        raise ValueError("Invalid format. The POS co chair name should be a string with at most 100 characters.")
    return value

def validate_country_citizenship(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 60:
        raise ValueError("Invalid format. The Country Citizenship should be a string with at most 60 characters.")
    return value

def validate_ethnicity(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 50:
        raise ValueError("Invalid format. The Ethnicity name should be a string with at most 50 characters.")
    return value

def validate_advisory_committee(value):
    if value is None:
        return value
    if not isinstance(value, str) or len(value) > 200:
        raise ValueError("Invalid format. The Advisers' Name should be a string with at most 200 characters.")
    return value
    
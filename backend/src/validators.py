from pydantic import EmailStr
from datetime import datetime

def validate_date(value):
        if value is None:
            return value
        try:
            value = datetime.strptime(value, '%d-%b-%y').date()
        except ValueError:
            raise ValueError("Invalid date format. Should be in the format '30-MAR-22'.")
        return value
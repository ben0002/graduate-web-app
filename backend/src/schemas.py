from pydantic import BaseModel
from pydantic.types import constr
from pydantic import EmailStr
from datetime import date

from enums import *

class Student(BaseModel):
    id: int
    first_name: str
    middle_name: str | None = None
    last_name: str
    va_residency: Residencies | None = None
    type: StudentTypes | None = None
    status: StudentStatus | None = None
    admit_type: AdmitType | None  = None
    campus_id: int | None = None
    email: EmailStr 
    phone_number: constr(
        pattern=r'^\(\d{3}\) \d{3}-\d{4}$',  # Regular expression pattern for (123) 456-7890
        strict=True,  # Enforce strict validation (default is False)
        strip_whitespace=True  # Remove leading/trailing whitespace (default is True)
    )
    visa_id: int
    pronouns: str
    advisory_committee: list[str]
    plan_submit_date: date
    prelim_exam_date: date
    prelim_exam_pass: date
    proposal_meeting: date
    progress_meeting: date
    ETD_submitted: bool
    final_exam: date
    first_term: int 
    profile_picture: str
    
    class Config:
        from_attributes = True
        

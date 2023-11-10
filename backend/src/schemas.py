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

class FileUpload(Student):
    email: str
    phone_number: str | None = None
    visa_id: int | None = None
    pronouns: str | None = None
    gender: str | None = None
    ethnicity: str | None = None
    advisory_committee: str | None = None
    plan_submit_date: str | None = None
    prelim_exam_date: str | None = None
    prelim_exam_pass: str | None = None
    proposal_meeting: str | None = None
    progress_meeting: str | None = None
    ETD_submitted: bool | None = None
    final_exam: str | None = None
    first_term: int | None = None
    profile_picture: str | None = None
    
        

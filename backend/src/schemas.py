from pydantic import BaseModel
from pydantic.types import constr
from pydantic import EmailStr
from datetime import date

from enums import *


class StudentIn(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    citizenship: str 
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
    ) | None = None
    #pronouns: str | None = None
    advisory_committee: str | None = None
    plan_submit_date: date | None = None
    prelim_exam_date: date | None = None
    prelim_exam_pass: date | None = None
    proposal_meeting: date | None = None
    progress_meeting: date | None = None
    ETD_submitted: bool | None = False
    final_exam: date | None = None
    first_term: int | None = None
    profile_picture: str | None = None
    
    class Config:
        from_attributes = True

class StudentOut(StudentIn):
    id: int
    
    class Config:
        from_attributes = True

class FacultyIn(BaseModel):
    first_name: str 
    middle_name: str | None = None
    last_name: str 
    dept_code: int # could be int or str; testing purposes = it is int rn
    faculty_type: str | None = None
    privilege_level: int | None = 1
    
    class Config:
        from_attributes = True
    
class FacultyOut(FacultyIn):
    id: int
    
    class Config:
        from_attributes = True

class Degree(BaseModel):
    id: int
    name: str
    description: str | None = None
    
    class Config:
        from_attributes = True

class Major(BaseModel):
    id: int
    name: str
    dept_code: int
    description: str | None = None
    
    class Config:
        from_attributes = True
    

class Token(BaseModel):
    access_token: str
    token_type: str


    
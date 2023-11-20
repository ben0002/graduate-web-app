from pydantic import BaseModel, validator, conint
from pydantic.types import constr
from pydantic import EmailStr
from fastapi import Field
from typing import Optional
from datetime import date
from validators import *
from enums import *


class VisaIn(BaseModel):
    
    student_id: int
    citizenship: str
    visa_name: str | None = None
    expiration_date: date | None = None
    
    class Config:
        from_attributes = True
        
class VisaOut(VisaIn):
    id: int
    
    class Config:
        from_attributes = True

class StudentIn(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=40)
    middle_name: str | None = None
    last_name: str = Field(..., min_length=1, max_length=40)
    va_residency: Residencies | None = None
    type: StudentTypes | None = None
    status: StudentStatus | None = None
    campus_id: int | None = None
    email: EmailStr 
    phone_number: constr(
        pattern=r'^\(\d{3}\) \d{3}-\d{4}$',  # Regular expression pattern for (123) 456-7890
        strict=True,  # Enforce strict validation (default is False)
        strip_whitespace=True  # Remove leading/trailing whitespace (default is True)
    ) | None = None
    pronouns: str | None = None
    advisory_committee: str = Field(None, max_length=200)
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

class FileUpload(StudentIn):
    pos_approveddate: date | None = None
    prelim_exam_date: date | None = None
    prelim_exam_pass: date | None = None
    #---------------------------Validator----------------------------------
    @validator("pos_approveddate", pre=True, always=True)
    def validate_pos_approveddate(cls, value):
        return validate_date(value)
    @validator("prelim_exam_date", pre=True, always=True)
    def validate_prelim_exam_date(cls, value):
        return validate_date(value)
    @validator("prelim_exam_pass", pre=True, always=True)
    def validate_prelim_exam_pass(cls, value):
        return validate_date(value)
    #--------------------------------------------------------------------------
    class Config:
        from_attributes = True

class FacultyIn(BaseModel):
    first_name: str 
    middle_name: str | None = None
    last_name: str 
    dept_code: str
    faculty_type: str | None = None
    privilege_level: int | None = 1
    
    class Config:
        from_attributes = True
    
class FacultyOut(FacultyIn):
    id: int
    
    class Config:
        from_attributes = True
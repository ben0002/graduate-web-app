from pydantic import BaseModel, validator, conint, Field
from pydantic.types import constr
from pydantic import EmailStr
from typing import Optional
from datetime import date
from validators import *
from enums import *


class StudentIn(BaseModel):
    first_name: str = Field(..., max_length=40)
    middle_name: Optional[str] = Field(None, max_length=40)
    last_name: str = Field(..., max_length=40)
    citizenship: Optional[str] = Field(None, max_length=60)
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
    pronouns: Optional[str] = Field(None, max_length=15)
    advisory_committee: Optional[str] = Field(None, max_length=200)
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

class StudentFileUpload(StudentIn):
    plan_submit_date: date | None = None
    prelim_exam_date: date | None = None
    prelim_exam_pass: date | None = None
    proposal_meeting: date | None = None
    progress_meeting: date | None = None
    final_exam: date | None = None
    #---------------------------Validator----------------------------------
    @validator("prelim_exam_date", pre=True, always=True)
    def validate_prelim_exam_date(cls, value):
        return validate_date(value)
    @validator("final_exam", pre=True, always=True)
    def validate_final_exam(cls, value):
        return validate_date(value)
    @validator("prelim_exam_pass", pre=True, always=True)
    def validate_prelim_exam_pass(cls, value):
        return validate_date(value)
    @validator("plan_submit_date", pre=True, always=True)
    def validate_plan_submit_date(cls, value):
        return validate_date(value)
    @validator("proposal_meeting", pre=True, always=True)
    def validate_proposal_meeting(cls, value):
        return validate_date(value)
    @validator("progress_meeting", pre=True, always=True)
    def validate_progress_meeting(cls, value):
        return validate_date(value)
    #--------------------------------------------------------------------------
    class Config:
        from_attributes = True

class FacultyIn(BaseModel):
    first_name: str = Field(..., max_length=40)
    middle_name: str | None = None
    last_name: str = Field(..., max_length=30)
    dept_code: int # could be int or str; testing purposes = it is int rn
    faculty_type: Optional[str] = Field(None, max_length=20)
    privilege_level: int | None = 1
    
    class Config:
        from_attributes = True
    
class FacultyOut(FacultyIn):
    id: int
    
    class Config:
        from_attributes = True

class DegreeIn(BaseModel):
    name: str = Field(..., max_length=30)
    description: Optional[str] = Field(None, max_length=500)
    
    class Config:
        from_attributes = True

class DegreeOut(DegreeIn):
    id: int
        
    class Config:
        from_attributes = True

class MajorIn(BaseModel):
    name: str = Field(..., max_length=30)
    dept_code: int
    description: str = Field(..., max_length=500)
    
    class Config:
        from_attributes = True

class MajorOut(MajorIn):
    id: int 
    class Config:
        from_attributes = True
    

class Token(BaseModel):
    access_token: str
    token_type: str

class CampusIn(BaseModel):
    name: str = Field(..., max_length=50)
    address: Optional[str] = Field(None, max_length=150)
    class Config:
        from_attributes = True
        
class CampusOut(CampusIn):
    id : int
    class Config:
        from_attributes = True
    
class DepartmentIn(BaseModel):
    name: str = Field(..., max_length=150)
    class Config:
        from_attributes = True
        
class DepartmentOut(DepartmentIn):
    dept_code: int
    class Config:
        from_attributes = True

    
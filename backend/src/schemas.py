from pydantic import BaseModel, validator, conint
from pydantic.types import constr
from pydantic import EmailStr
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
    first_name: str
    middle_name: str | None = None
    last_name: str
    va_residency: Residencies | None = None
    type: StudentTypes | None = None
    status: StudentStatus | None = None
    # admit_type: AdmitType | None  = None
    campus_id: int | None = None
    email: EmailStr 
    phone_number: constr(
        pattern=r'^\(\d{3}\) \d{3}-\d{4}$',  # Regular expression pattern for (123) 456-7890
        strict=True,  # Enforce strict validation (default is False)
        strip_whitespace=True  # Remove leading/trailing whitespace (default is True)
    )
    visa: VisaIn | None = None
    pronouns: str | None = None
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

class FileUpload(StudentIn):
    email: EmailStr
    phone_number: constr(
        pattern=r'^\(\d{3}\) \d{3}-\d{4}$',  # Regular expression pattern for (123) 456-7890
        strict=True,  # Enforce strict validation (default is False)
        strip_whitespace=True # Remove leading/trailing whitespace (default is True)      
    ) | None = None
    #visa_id: int | None = None not sure if we stil need it 
    #pronouns: str | None = None dk we need it or not
    campus: int # it will be number 0, 10, 4 which mapped to campus name, you could change it to be str when the data has name on campus as string.
    gender: str | None = None
    ethnicity: str | None = None
    admit_camp: str | None = None
    level: DegreeLevels | None = None
    degree_name: str | None = None
    major_name: str | None = None
    major_description: str | None = None
    first_term: int | None = None
    pos_approveddate: date | None = None
    pos_chair: str | None = None
    pos_co_chair: str | None = None
    country_citizenship: str | None = None
    advisory_committee: str | None = None
    prelim_exam_date: date | None = None
    prelim_exam_pass: date | None = None
    #---------------------------Validator----------------------------------
    @validator("first_name", pre=True, always=True)
    def validate_firstname(cls, value):
        return validate_firstname(value)
    @validator("middle_name", pre=True, always=True)
    def validate_middlename(cls, value):
        return validate_middlename(value)
    @validator("last_name", pre=True, always=True)
    def validate_lastname(cls, value):
        return validate_lastname(value)
    @validator("admit_camp", pre=True, always=True)
    def validate_admitcamp(cls, value):
        return validate_admitcamp(value)
    @validator("degree_name", pre=True, always=True)
    def validate_degreename(cls, value):
        return validate_degreename(value)
    @validator("major_description", pre=True, always=True)
    def validate_majordescription(cls, value):
        return validate_majordescription(value)
    @validator("first_term", pre=True, always=True)
    def validate_firstterm(cls, value):
        return validate_firstterm(value)
    @validator("pos_approveddate", pre=True, always=True)
    def validate_pos_approveddate(cls, value):
        return validate_date(value)
    @validator("pos_chair", pre=True, always=True)
    def validate_pos_chair(cls, value):
        return validate_pos_chair(value)
    @validator("pos_co_chair", pre=True, always=True)
    def validate_pos_co_chair(cls, value):
        return validate_pos_co_chair(value)
    @validator("country_citizenship", pre=True, always=True)
    def validate_country_citizenship(cls, value):
        return validate_country_citizenship(value)
    @validator("ethnicity", pre=True, always=True)
    def validate_ethnicity(cls, value):
        return validate_ethnicity(value)
    @validator("advisory_committee", pre=True, always=True)
    def validate_advisory_committee(cls, value):
        return validate_advisory_committee(value)
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
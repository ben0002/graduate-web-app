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
    graduation_date: date | None = None
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
        
class CreateStudent(StudentIn):
    major_name : str = Field(..., max_length=30)
    degree_name : str = Field(..., max_length=30)
    enrollment_date : date | None = None
    advisor_first_name : str = Field(..., max_length=40)
    advisor_midlle_name : Optional[str] = Field(None, max_length=40)
    advisor_last_name : str = Field(..., max_length=40)
    campus_name: str = Field(..., max_length=50)
    co_advisor_name: str | None = None
    
    class Config:
        from_attributes = True

class StudentFileUpload(StudentIn):
    #---------------------------Validator----------------------------------
    @validator("graduation_date", pre=True, always=True)
    def validate_graduation_date(cls, value):
        return validate_date(value)
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
    email: EmailStr
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
        
class ProgramEnrollmentIn(BaseModel):
    student_id: int
    degree_id: int
    major_id: int
    enrollment_date: date
    @validator("enrollment_date", pre=True, always=True)
    def validate_enrollment_date(cls, value):
        return validate_date(value)
    class Config:
        from_attributes = True

class ProgramEnrollmentOut(BaseModel):
    id: int
    major: MajorOut
    degree: DegreeOut
    enrollment_date: date
    

class StudentLabsIn(BaseModel):
    student_id: int
    name: str = Field(..., max_length=40)
    director: str = Field(..., max_length=40)
    class Config:
        from_attributes = True
        
class StudentLabsOut(StudentLabsIn):
    id : int
    class Config:
        from_attributes = True
        
class StudentAdvisorIn(BaseModel):
    advisor_role : AdvisorRole
    class Config:
        from_attributes = True

class CreateStudentAdvisor(StudentAdvisorIn):
    advisor_name : str = Field(..., max_length=120)
        
class StudentAdvisorOut(StudentAdvisorIn, FacultyOut):
    
    class Config:
        from_attributes = True
        
class EmploymentIn(BaseModel):
    student_id : int
    job_title : str = Field(..., max_length=40)
    pay : int | None = None
    start_date: date | None = None
    end_date : date | None = None
    type : str = Field(..., max_length=30)
    class Config:
        from_attributes = True

class EmploymentOut(EmploymentIn):
    id : int
    class Config:
        from_attributes = True

class FundingIn(BaseModel):
    student_id : int
    name : str = Field(..., max_length=50)
    award_amount : int | None = None
    start_date: date | None = None
    end_date : date | None = None
    guaranteed : bool | None = False    
    class Config:
        from_attributes = True
        
class FundingOut(FundingIn):
    id : int 
    class Config:
        from_attributes = True

class EventIn(BaseModel):
    student_id : int
    name : str = Field(..., max_length=40)
    due_date: date | None = None
    description : Optional[str] = Field(None, max_length=100)
    status: EventStatus
    class Config:
        from_attributes = True

class EventOut(EventIn):
    id : int
    class Config:
        from_attributes = True

class RequirementIn(BaseModel):
    name : str = Field(..., max_length=50)
    description : Optional[str] = Field(None, max_length=100)
    major_id: int
    degree_id: int
    class Config:
        from_attributes = True
        
class RequirementOut(RequirementIn):
    id : int
    class Config:
        from_attributes = True

class MilestoneIn(BaseModel):
    name : str = Field(..., max_length=50)
    description : Optional[str] = Field(None, max_length=100)
    major_id: int
    degree_id: int
    class Config:
        from_attributes = True
        
class MilestoneOut(MilestoneIn):
    id : int
    class Config:
        from_attributes = True

class CreateMilestone(MilestoneIn):
    major_name : str = Field(..., max_length=30)
    degree_name : str = Field(..., max_length=30)
    class Config:
        from_attributes = True

class ProgressIn(BaseModel):
    student_id : int
    ideal_completion_date: date | None = None
    requirement_id: int | None = None
    milestone_id: int | None = None
    deadline: date | None = None
    completion_date: date | None = None
    approved: bool | None = False
    note : Optional[str] = Field(None, max_length=200)
    exempt: bool | None = False
    
    class Config:
        from_attributes = True

class ProgressOut(BaseModel):
    id : int
    ideal_completion_date: date | None = None
    deadline: date | None = None
    completion_date: date | None = None
    approved: bool | None = False
    exempt: bool | None = False
    note: Optional[str] = Field(None, max_length=200)
    requirement: RequirementOut | None = None
    milestone: MilestoneOut | None = None
    
    class Config:
        from_attributes = True
        exclude_unset = True  # Exclude fields with None (null) values

class CreateRequirement(RequirementIn):
    major_name : str = Field(..., max_length=30)
    degree_name : str = Field(..., max_length=30)
    class Config:
        from_attributes = True

class CourseEnrollmentIn(BaseModel):
    student_id: int
    course_title: str = Field(..., max_length=50)   
    course_type: CourseType
    credits: int
    term: int
    pos_id: int | None = None
    year: int | None = None
    class Config:
        from_attributes = True

class CourseEnrollmentOut(CourseEnrollmentIn):
    id: int
    class Config:
        from_attributes = True
        
        
class StudentPOSIn(BaseModel):
    student_id: int
    approved: bool | None = False
    approved_date: Optional[str] = Field(None, max_length=50)
    chair: Optional[str] = Field(None, max_length=100)
    co_chair: Optional[str] = Field(None, max_length=100)
    class Config:
        from_attributes = True

class StudentPOSOut(StudentPOSIn):
    id: int
    class Config:
        from_attributes = True


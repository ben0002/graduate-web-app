from pydantic import BaseModel, validator, Field
from pydantic.types import constr
from pydantic import EmailStr
from typing import Optional
from datetime import date
from validators import *
from enums import *

# clean up dates and just require one date format

#---------------------- student schemas -----------------------------#

class StudentIn(BaseModel):
    first_name: str = Field(..., max_length=40)
    middle_name: Optional[str] = Field(None, max_length=40)
    last_name: str = Field(..., max_length=40)
    citizenship: str | None = Field(default="United States of America", max_length=60)
    va_residency: Residencies | None = None
    status: StudentStatus | None = None
    campus_id: int | None = None
    email: EmailStr 
    phone_number: constr(
        pattern=r'^\(\d{3}\) \d{3}-\d{4}$',  # Regular expression pattern for (123) 456-7890
        strict=True,  # Enforce strict validation (default is False)
        strip_whitespace=True  # Remove leading/trailing whitespace (default is True)
    ) | None = None
    pronouns: Optional[str] = Field(None, max_length=15)
    gender: Optional[str] = Field(None, max_length=10)
    advisory_committee: Optional[str] = Field(None, max_length=200)
    plan_submit_date: date | None = None
    prelim_exam_date: date | None = None
    prelim_exam_pass: date | None = None
    proposal_meeting: date | None = None
    progress_meeting: date | None = None
    graduation_date: date | None = None
    ETD_submitted: bool | None = False
    final_exam: date | None = None
    enrollment_term: AcademicTerm | None = None
    enrollment_year: int | None = None
    profile_picture: str | None = None
    class Config:
        from_attributes = True

class StudentOut(StudentIn):
    id: int
    
    class Config:
        from_attributes = True

class CreateProgramEnrollment(BaseModel):
    major_id: int
    degree_id: int
    concentration: str | None = None  
    enrollment_date: date

class StudentAdvisor(BaseModel):
    first_name: str = Field(..., max_length=40)
    last_name : str = Field(..., max_length=40)
    
class CreateStudent(StudentIn):
    program_enrollments: list[CreateProgramEnrollment]
    main_advisor_id: int 
    co_advisors_ids: list[int] | None = None
    campus_id: int 
    
    class Config:
        exclude = ['campus_id', 'profile_picture']

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
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class DegreeOut(DegreeIn):
    id: int
        
    class Config:
        from_attributes = True

class MajorIn(BaseModel):
    name: str = Field(..., max_length=30)
    dept_code: int
    description: str = None
    
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
    concentration: str | None = None
    enrollment_date: date
    
    class Config:
        from_attributes = True

class ProgramEnrollmentFileIn(ProgramEnrollmentIn):
    @validator("enrollment_date", pre=True, always=True)
    def validate_enrollment_date(cls, value):
        return validate_date(value)
    

class ProgramEnrollmentOut(BaseModel):
    id: int
    major: MajorOut
    degree: DegreeOut
    concentration: str | None
    enrollment_date: date
    

class StudentLabsIn(BaseModel):
    student_id: int
    name: str = Field(..., max_length=40)
    director: str = Field(..., max_length=40)
    start_date: date | None = None
    location: str = Field(None, max_length=50)
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
    start_date: date 
    end_date : date | None = None
    guaranteed : bool | None = False
    recurring: bool | None = False
    description: str | None = None
    notes: str | None = None    
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
    description : Optional[str] = None
    status: EventStatus
    class Config:
        from_attributes = True

class EventOut(EventIn):
    id : int
    class Config:
        from_attributes = True

class RequirementIn(BaseModel):
    name : str = Field(..., max_length=50)
    description : Optional[str] = None
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
    description : Optional[str] = None
    major_id: int
    degree_id: int
    class Config:
        from_attributes = True
        
class MilestoneOut(MilestoneIn):
    id : int
    class Config:
        from_attributes = True


class ProgressIn(BaseModel):
    student_id : int
    ideal_completion_date: date | None = None
    requirement_id: int | None = None
    milestone_id: int | None = None
    custom_milestone_name: str | None = None
    custom_milestone_description: str | None = None
    deadline: date | None = None
    completion_date: date | None = None
    approved: bool | None = False
    note : Optional[str] | None = None
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
    note: Optional[str] | None = False
    requirement: RequirementOut | None = None
    milestone: MilestoneOut | None = None
    custom_milestone_name: str | None = None
    custom_milestone_description: str | None = None
    
    class Config:
        from_attributes = True
        exclude_unset = True  # Exclude fields with None (null) values

class CourseEnrollmentIn(BaseModel):
    student_id: int
    course_title: str = Field(..., max_length=50)   
    transfer: bool = False
    credits: int
    term: int
    pos_id: int | None = None
    year: int | None = None
    research: bool | None = False
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
    status: POSStatus | None = POSStatus.WAITING_APPROVAL
    class Config:
        from_attributes = True

class StudentPOSOut(StudentPOSIn):
    id: int
    class Config:
        from_attributes = True


# ----------------------- lump schemas ------------------------- #
class studentCard(BaseModel):
    info: StudentOut
    campus: CampusOut
    advisors: list[StudentAdvisorOut]
    programs: list[ProgramEnrollmentOut]
    pos: list[StudentPOSOut]
    
class progressPage(BaseModel):
    #   To do box --> events
    #Milestones --> milestones progress
    #Requirements --> requirement progress
    #Funding --> funding 
    #Employment --> employment
    milestones: list[ProgressOut]
    requirements: list[ProgressOut]
    funding: list[FundingOut]
    employment: list[EmploymentOut]
    to_do_list: list[EventOut]
    courses: list[CourseEnrollmentOut]
    
class ProfilePage(BaseModel):
    # add messages once table is in
    advisors: list[StudentAdvisorOut]
    advisory_committee: str | None = ""
    labs: list[StudentLabsIn]
    courses: list[CourseEnrollmentOut] 
    

class MessageOut(BaseModel):
    id: int 
    student_id: int
    advisor_id: int | None = None
    text: str
    private: bool | None = False
    

    
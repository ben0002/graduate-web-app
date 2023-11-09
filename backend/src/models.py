""" defines the models (tables) that are part of our database. Illustrates 
the schema """

from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Enum
from database import engine
from enums import *


class Base(DeclarativeBase):
    """ Creates the base class that inherit DeclarativeBase which
    which allows for ORM and our database structure to be created.
    
    Returns: None
    """

class Student(Base):
    """Models the student table in the database that contains information about all
    students.
        student's
        - first name
        - last name
        - middle name
        - residency
        - type
        - status
        - admit type
        - campus id
        - email
        - phone number
        - citizenship
        - gender
        - ethnicity
        - committee members
        - prelim exam date
        - prelim exam pass
        - first term 
        - profile picture

    Args:
        Base: Inherited superclass that allows ORM
    """
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40))
    middle_name: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(40))
    va_residency: Mapped[Residencies] = mapped_column(Enum(Residencies), nullable=True)
    type: Mapped[StudentTypes] = mapped_column(Enum(StudentTypes), nullable=True)
    status: Mapped[StudentStatus] = mapped_column(Enum(StudentStatus), nullable=True)
    # admit_type: Mapped[AdmitType] = mapped_column(Enum(AdmitType), nullable=True)
    campus_id: Mapped[Optional[int]] = mapped_column(Integer,ForeignKey("campus.id"), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(70))
    phone_number: Mapped[Optional[str]] = mapped_column(String(13), nullable=True) 
    pronouns: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    # gender : Mapped[str] = mapped_column(String(40)) 
    # ethnicity : Mapped[str] = mapped_column(String(50)) 
    advisory_committee : Mapped[Optional[str]] = mapped_column(String(200), nullable=True) 
    prelim_exam_date : Mapped[Optional[str]] = mapped_column(String(10), nullable=True) # do we drop this column?
    plan_submit_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    prelim_exam_pass: Mapped[Optional[str]] = mapped_column(String(10), nullable=True) 
    proposal_meeting: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    progress_meeting: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    ETD_submitted: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    final_exam: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    first_term : Mapped[int] = mapped_column(Integer, nullable=True) 
    profile_picture : Mapped[Optional[str]] = mapped_column(String(100), nullable=True) 
    
    
    campus = relationship("Campus", back_populates = "students") 
    employment = relationship("Employment", back_populates = "student") 
    funding = relationship("Funding", back_populates = "student") 
    advisors = relationship("StudentAdvisor", back_populates = "student") 
    events = relationship("Event", back_populates = "student") 
    labs = relationship("StudentLabs", back_populates = "student") 
    programs = relationship("ProgramEnrollment", back_populates = "student") 
    progress_tasks = relationship("Progress", back_populates = "student") 
    courses = relationship("CourseEnrollment", back_populates = "student") 
    pos = relationship("StudentPOS", back_populates = "student") 
    visa = relationship("Visa", back_populates="student") 
    
    def __repr__(self) -> str:
        return f"Student(id={self.id!r}, name={self.first_name!r}, lastname={self.last_name!r}, email={self.email!r})"
    
class Degree(Base):
    """Represents the table that stores degree info: 
       - degree name (unique)
       - degree level (unique)
       - degree description

    Args:
        Base: Inherited base class that allows ORM.
    """
    __tablename__ = "degree"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    level: Mapped[DegreeLevels] = mapped_column(Enum(DegreeLevels))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
     # way to list multiple unique constraints that are constrained together
     # make sure that the degree name and degree level should be unique to each other.
    __table_args__ = (UniqueConstraint('name', 'level', name='degree_name_level_uc'),)
    
    requirements = relationship("Requirement", back_populates="degree") 
    

    def __repr__(self) -> str:
        return f"Degree(id={self.id!r}, name={self.name!r}, level={self.level!r}, description={self.description!r})"
    
class Major(Base):
    """Represents the table that stores info about all available majors:
        - name
        - description
        - department 
    
    Args:
        Base: Inherited base class that allows ORM.
    """
    
    __tablename__ = "major"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    dept_code: Mapped[str] = mapped_column(String(10), ForeignKey("department.dept_code"))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    department = relationship("Department", back_populates="majors") 
    requirements = relationship("Requirement", back_populates="major") 
    
    def __repr__(self) -> str:
        return f"Major(id={self.id!r}, name={self.name!r}, dept_code={self.dept_code!r}, description={self.description!r})"
    
class Department(Base):
    """Table that holds information about all departments.
        - name
    Args:
        Base: Inherited base class that allows ORM
    """
    
    __tablename__ = "department"
    
    dept_code: Mapped[str] = mapped_column(String(7), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
    faculty = relationship("Faculty", back_populates="department")
    majors = relationship("Major", back_populates="department") 
    
    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, name={self.name!r})"

class ProgramEnrollment(Base):
    """Holds information of student program enrollments by storing:
        - Unique combination of:
            - Degree
            - Major
            - Student id
        - enrollment date

    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = "program_enrollment"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    degree_id: Mapped[int] = mapped_column(Integer, ForeignKey("degree.id"))
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey("major.id"))
    enrollment_date: Mapped[str] = mapped_column(String(10))
    
    # way to list multiple unique constraints that are constrained together
    __table_args__ = (UniqueConstraint('student_id', 'degree_id', 'major_id', name='program_student_degree_major_uc'),)
    
    student = relationship("Student", back_populates="programs")
        
    def __repr__(self) -> str:
        return f"ProgramEnrollments(id={self.id!r}, student_id={self.student_id!r}, degree_id={self.degree_id!r}, major_id={self.major_id!r})"
    
class StudentLabs(Base):
    """Holds information of student labs:
        - student id
        - name
        - director name

    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = 'student_labs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    name: Mapped[str] = mapped_column(String(40))
    director: Mapped[str] = mapped_column(String(40))
    
    student = relationship("Student", back_populates="labs")
    
    def __repr__(self) -> str:
        return f"StudentLabs(id={self.id!r}, student_id={self.student_id!r}, name={self.name!r})"

class StudentAdvisor(Base):
    """Holds information of student's advisors:
        - student id & faculty id (composite primary key)
        - advisor role
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = 'student_advisor'
    advisor_id: Mapped[int] = mapped_column(Integer, ForeignKey('faculty.id'))
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('student.id'))
    advisor_role: Mapped[AdvisorRole] = mapped_column(Enum(AdvisorRole))
    
    __table_args__ = (
        PrimaryKeyConstraint('advisor_id', 'student_id'),
    )
    
    student = relationship("Student", back_populates="advisors")

    def __repr__(self) -> str:
        return f"StudentAdvisor(advisor_id={self.id!r}, student_id={self.student_id!r}, advisor_role={self.advisor_role!r})"

class Visa(Base):
    """Holds Visa information from student:
        - citizenship
        - visa name
        - expiration date
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'visa'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id", name="visa-student"), unique=True)
    citizenship: Mapped[str] = mapped_column(String(60))
    visa_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    expiration_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True) # integer (mmddyyyy)
    
    student = relationship("Student", back_populates = "visa") 

    def __repr__(self) -> str:
        return f"Visa(student_id={self.student_id!r}, visa_name={self.visa_name!r}, expiration_date: {self.expiration_date})"

class Campus(Base):
    """Holds Campus information from student:
        - name
        - address
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = 'campus'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    
    students = relationship("Student", back_populates="campus")
    
    def __repr__(self) -> str:
        return f"Campus(id={self.id!r}, name={self.name!r}, address={self.address})"

class Employment(Base):
    """Holds Employment information from student:
        - student id
        - job title
        - salary
        - start date
        - end date
        - type
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'employment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    job_title: Mapped[str] = mapped_column(String(40))
    pay: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) 
    start_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True) 
    end_date : Mapped[Optional[str]] = mapped_column(String(10), nullable=True)    
    type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    student = relationship("Student", back_populates = "employment")

    def __repr__(self) -> str:
        return f"Employment(id={self.id!r}, job_title={self.job_title!r})"

class Funding(Base):
    """Holds Funding information:
        - student id
        - name of funding
        - the award amount
        - start date
        - end date
        - guaranteed
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'funding'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    name: Mapped[str] = mapped_column(String(50))
    award_amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) 
    start_date: Mapped[str] = mapped_column(String(10)) 
    end_date: Mapped[str] = mapped_column(String(10))   
    guaranteed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)  

    student = relationship("Student", back_populates="funding")

    def __repr__(self) -> str:
        return f"Funding(id={self.id!r}, name={self.name!r})"

class Event(Base):
    """Holds Funding information:
        - student id
        - name of event
        - due date
        - description
        - status of event
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'event'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    name: Mapped[str] = mapped_column(String(40))
    due_date: Mapped[str] = mapped_column(String(10))   #July dd,yyyy
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus)) #Complete, On-Going
    
    student = relationship("Student", back_populates="events")
    
    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, name={self.name!r})"

class Faculty(Base):
    """Holds faculty information:
        - first name
        - middle name
        - last name
        - department id or department code
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = 'faculty'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40))
    middle_name: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(40))
    dept_code: Mapped[String] = mapped_column(String(7), ForeignKey("department.dept_code"))
    faculty_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    privilege_level: Mapped[int] = mapped_column(Integer)
    
    department = relationship("Department", back_populates="faculty")
    
    def __repr__(self) -> str:
        return f"Faculty(id={self.id!r},first_name={self.first_name!r},last_name={self.last_name!r})"

class Requirement(Base):
    """Holds requirement:
        - name
        - description
        - major id 
        - degree id
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = 'requirement'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey("major.id"))
    degree_id: Mapped[int] = mapped_column(Integer, ForeignKey("degree.id"))
    
    degree = relationship("Degree", back_populates="requirements")
    major = relationship("Major", back_populates="requirements")
    
    
    def __repr__(self) -> str:
        return f"Requirement(id={self.id!r},name={self.name!r})"

class Milestone(Base):
    """Holds the information of milestone:
        - name
        - description
        - stage id ----- do we still need it?
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'milestone'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey("stage.id"))
    
    stage = relationship("Stage", back_populates="milestones")
    
    def __repr__(self) -> str:
        return f"Milestone(id={self.id!r},name={self.name!r})"

class Progress(Base):
    """Holds the information of progress from student:
        - name
        - requirement id
        - milestone id
        - ideal completion date
        - deadline
        - completion date
        - approved
        - notes
        - student id
        - exempt
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'progress'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    ideal_completion_date: Mapped[str] = mapped_column(String(10))
    requirement_id: Mapped[int] = mapped_column(Integer, ForeignKey("requirement.id"))
    milestone_id: Mapped[int] = mapped_column(Integer, ForeignKey("milestone.id"))
    deadline: Mapped[str] = mapped_column(String(10))
    completion_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    approved: Mapped[bool] = mapped_column(Boolean)
    note: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    exempt: Mapped[bool] = mapped_column(Boolean)
    
    
    student = relationship("Student", back_populates="progress_tasks")
    
    def __repr__(self) -> str:
        return f"Progress(id={self.id!r},requirement_id={self.requirement_id!r},student_id={self.student_id!r})"

class CourseEnrollment(Base):
    """Holds the information of course enrollment from student:
        - course title
        - course type
        - credit
        - term
        - student id
        - POS id for Plan of Study table
        - year
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'course_enrollment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    course_title: Mapped[str] = mapped_column(String(50))    
    course_type: Mapped[CourseType] = mapped_column(Enum(CourseType)) 
    credits: Mapped[int] = mapped_column(Integer)
    term: Mapped[int] = mapped_column(Integer)
    pos_id: Mapped[int] = mapped_column(Integer, ForeignKey("student_pos.id"))
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # Do We need the years for the CourseEnrollment? add it just in case we need
    
    student = relationship("Student", back_populates="courses")
    student_pos = relationship("StudentPOS", back_populates="courses")
    
    
    def __repr__(self) -> str:
        return f"CourseEnrollment(id={self.id!r},student_id={self.student_id!r},course_title={self.course_title!r})"
        
class Stage(Base): 
    """Holds the stage information:
        - name
        - description
        - major id
        - degree id
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'stage'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey("major.id"))
    degree_id: Mapped[int] = mapped_column(Integer, ForeignKey("degree.id"))
    
    milestones = relationship("Milestone", back_populates="stage")
    
    
    def __repr__(self) -> str:
        return f"Stage(id={self.id!r},major_id={self.major_id!r},degree_id={self.degree_id!r})"

class StudentPOS(Base):
    """Holds the information of student pos (Plan of Study):
        - on file
        - student id
        - approved
        - name of chair
        - name of co-chair
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    __tablename__ = 'student_pos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    approved: Mapped[bool] = mapped_column(Boolean)
    chair: Mapped[str] = mapped_column(String(100))
    co_chair: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    student = relationship("Student", back_populates="pos")
    courses = relationship("CourseEnrollment", back_populates="student_pos")
    
    def __repr__(self) -> str:
        return f"StudentPOS(id={self.id!r},student_id={self.student_id!r})"

    
    


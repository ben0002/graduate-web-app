""" defines the models (tables) that are part of our database. Illustrates 
the schema """

import enum
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Enum
from database import engine

class DegreeLevels(enum.Enum):
    """Valid values for degree levels.
    """
    REGULAR_MASTERS = 1
    DOCTORAL = 2
    PROVISIONAL_MASTERS = 3
    REGULAR_POST_MASTERS = 4

class CourseType(enum.Enum):
    """Valid values for if the course is transfer or not From Course Enrollment.
    """
    TRANSFER = 1
    NOT_TRANSFER = 2
    
    
class Term(enum.Enum):
    """Valid values for the term of course.
    """
    Term_1 = 1
    Term_2 = 2
    Term_3 = 3
    Term_4 = 4
    
class Exempt(enum.Enum):
    """Valid values for status of exempt for the progress.
    """
    NOT_EXEMPT = 1
    EXEMPT = 2
    
class Approve(enum.Enum):
    """Valid values for approve status for progress and POS.
    """
    NOT_APPPROVED = 1
    APPROVED = 2
    
class Status(enum.Enum):
    """Valid values for status of event.
    """
    ON_GOING = 1
    COMPLETE = 2
    
class Guaranteed(enum.Enum):
    """Valid values for Guaranteed of funding.
    """
    NO = 1
    YES = 2
    
class AdvisorRole(enum.Enum):
    """Valid values for Advisor Role.
    """
    MAIN_ADVISOR = 1
    CO_ADVISOR = 2
    
    
class Ethnicity(enum.Enum):
    """Valid values for Ethnicity of student.
    """
    CAUCASIAN = 1
    ASIAN_OR_PACIFIC_ISLANDER = 2
    BLACK = 3
    HISPANIC = 4
    NOT_REPORT = 5
    
class Gender(enum.Enum):
    """Valid values for gender of student.
    """
    MALE = "M"
    FEMALE = "F"
    
class Residencies(enum.Enum):
    """Values that are valid for residencies of student.
    """
    IN_STATE = "in state"
    OUT_OF_STATE = "out of state"
    
class StudentStatus(enum.Enum):
    """Values that are valid for student status'.
    """
    STATUS_1 = 1
    STATUS_2 = 2
    STATUS_3 = 3

class AdmitType(enum.Enum):
    """Values that are valid for admission types of students.
    """
    ADMIT_1 = 1
    ADMIT_2 = 2
    ADMIT_3 = 3

class StudentTypes(enum.Enum):
    """Values that are valid for the different student types.
    """
    NEW = 1
    CONT = 2
    NEW_PROGRAM = 3

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
    residency: Mapped[Residencies] = mapped_column(Enum(Residencies), nullable=True)
    type: Mapped[StudentTypes] = mapped_column(Enum(StudentTypes), nullable=True)
    status: Mapped[StudentStatus] = mapped_column(Enum(StudentStatus), nullable=True)
    admit_type: Mapped[AdmitType] = mapped_column(Enum(AdmitType), nullable=True)
    campus_id: Mapped[int] = mapped_column(Integer,ForeignKey("campus.id"),nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String)
    phone_numer: Mapped[Optional[str]] = mapped_column(String, nullable=True) # (540)855-1524, could be empty
    citizenship: Mapped[Optional[str]] = mapped_column(String)
    gender : Mapped[Gender] = mapped_column(Enum(Gender))
    ethnicity : Mapped[Ethnicity] = mapped_column(Enum(Ethnicity)) # not sure about it.They can have mutiple ethnicity like Caucasian, Asian/Pacific islander
    committee_members : Mapped[Optional[str]] = mapped_column(String, nullable=True) 
    prelim_exam_date : Mapped[Optional[str]] = mapped_column(String, nullable=True) #11-SEP-23
    prelim_exam_pass : Mapped[Optional[str]] = mapped_column(String, nullable=True) #11-SEP-23
    first_term : Mapped[int] = mapped_column(Integer, nullable=True) #202209 or may have empty
    profile_picture : Mapped[Optional[str]] = mapped_column(String, nullable=True) #file path. or they do not have picture
    #addresses: Mapped[List["Address"]] = relationship(back_populates="user")

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
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    level: Mapped[DegreeLevels] = mapped_column(Enum(DegreeLevels), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    
     # way to list multiple unique constraints that are constrained together
     # make sure that the degree name and degree level should be unique to each other.
    __table_args__ = (UniqueConstraint('name', 'level', name='degree_name_level_uc'),)

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
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    dept_id: Mapped[int] = mapped_column(ForeignKey("department.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    
    def __repr__(self) -> str:
        return f"Major(id={self.id!r}, name={self.name!r}, dept_id={self.dept_id!r}, description={self.description!r})"
    
class Department(Base):
    """Table that holds information about all departments.
        - name
    Args:
        Base: Inherited base class that allows ORM
    """
    
    __tablename__ = "department"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, name={self.name!r})"

class ProgramEnrollments(Base):
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
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"), nullable=False)
    degree_id: Mapped[int] = mapped_column(Integer, ForeignKey("degree.id"), nullable=False)
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey("major.id"), nullable=False)
    enrollment_date: Mapped[Optional[str]] = mapped_column(String)
    
    # way to list multiple unique constraints that are constrained together
    __table_args__ = (UniqueConstraint('student_id', 'degree_id', 'major_id', name='program_student_degree_major_uc'),)
    
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
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"), nullable=False)
    name: Mapped[int] = mapped_column(String)
    director: Mapped[Optional[str]] = mapped_column(String)
    
    def __repr__(self) -> str:
        return f"StudentLabs(id={self.id!r}, student_id={self.student_id!r}, name={self.name!r})"

class StudentAdvisors(Base):
    """Holds information of student's advisors:
        - student id (primary key)
        - advisor role
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = 'student_advisors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    advisor_role: Mapped[AdvisorRole] = mapped_column(Enum(AdvisorRole))
    
    def __repr__(self) -> str:
        return f"StudentAdvisors(id={self.id!r}, student_id={self.student_id!r}, advisor_role={self.advisor_role!r})"

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
    citizenship: Mapped[Optional[str]] = mapped_column(String)
    visa_name: Mapped[Optional[str]] = mapped_column(String)
    expiration_date: Mapped[Optional[str]] = mapped_column(String) # either integer (mmddyyyy) or string (mm/dd/yyyy)

    def __repr__(self) -> str:
        return f"Visa(id={self.id!r}, visa_name={self.visa_name!r})"

class Campus(Base):
    """Holds Campus information from student:
        - name
        - address
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = 'campus'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    def __repr__(self) -> str:
        return f"Campus(id={self.id!r}, name={self.name!r})"

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
    job_title: Mapped[Optional[str]] = mapped_column(String)
    pay: Mapped[int] = mapped_column(Integer, nullable=True) #may have empty
    start_date: Mapped[Optional[str]] = mapped_column(String, nullable=True) #July dd,yyyy
    end_date : Mapped[Optional[str]] = mapped_column(String, nullable=True)   #July dd,yyyy 
    type: Mapped[Optional[str]] = mapped_column(String, nullable=True)

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
    funding_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    name: Mapped[Optional[str]] = mapped_column(String)
    award_amount: Mapped[int] = mapped_column(Integer, nullable=True) #may have empty
    start_date: Mapped[Optional[str]] = mapped_column(String) #July dd,yyyy
    end_date: Mapped[Optional[str]] = mapped_column(String)   #July dd,yyyy
    guaranteed: Mapped[Guaranteed] = mapped_column(Enum(Guaranteed)) # not sure 

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
    name: Mapped[Optional[str]] = mapped_column(String)
    due_date: Mapped[Optional[str]] = mapped_column(String)   #July dd,yyyy
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[Status] = mapped_column(Enum(Status)) #Complete, On-Going
    
    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, name={self.name!r})"

class Advisor(Base):
    """Holds advisor information:
        - first name
        - middle name
        - last name
        - department id or department code
        
    Args:
        Base: Inherited base class from SQLAlchemy that allows ORM
    """
    
    __tablename__ = 'advisor'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40))
    middle_name: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(40))
    dept_id: Mapped[int] = (Integer, ForeignKey("department.id"))
    
    def __repr__(self) -> str:
        return f"Advisor(id={self.id!r},first_name={self.first_name!r},last_name={self.last_name!r})"

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
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    degree_id: Mapped[int] = mapped_column(Integer, ForeignKey("degree.id"))
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey("major.id"))
    
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
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey("stage.id"))
    
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
    requirement_id: Mapped[int] = mapped_column(Integer, ForeignKey("requirement.id"))
    milestone_id: Mapped[int] = mapped_column(Integer, ForeignKey("milestone.id"))
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id"))
    ideal_completion_date: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    deadline: Mapped[Optional[str]] = mapped_column(String)
    completion_date: Mapped[Optional[str]] = mapped_column(String)
    approve: Mapped[Approve] = mapped_column(Enum(Approve))
    note: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    exempt: Mapped[Exempt] = mapped_column(Enum(Exempt))
    
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
    course_title: Mapped[Optional[str]] = mapped_column(String)    
    course_type: Mapped[CourseType] = mapped_column(Enum(CourseType)) 
    credits: Mapped[int] = mapped_column(Integer)
    term: Mapped[Term] = mapped_column(Enum(Term))
    pos_id: Mapped[int] = mapped_column(Integer, ForeignKey("studentpos.id"))
    year: Mapped[int] = mapped_column(Integer, nullable=True) # Do We need the years for the CourseEnrollment? add it just in case we need
    
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
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey("major.id"))
    degree_id: Mapped[int] = mapped_column(Integer, ForeignKey("degree.id"))
    
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
    approved: Mapped[Approve] = mapped_column(Enum(Approve))
    chair: Mapped[Optional[str]] = mapped_column(String)
    co_chair: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    def __repr__(self) -> str:
        return f"StudentPOS(id={self.id!r},student_id={self.student_id!r})"

    
    
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
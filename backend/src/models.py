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
    

class Residencies(enum.Enum):
    """Values that are valid for residencies.
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
      
    #addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.first_name!r}, lastname={self.last_name!r})"
    
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
    
    # way to list multiple unique constraints that are constrained together
    __table_args__ = (UniqueConstraint('student_id', 'degree_id', 'major_id', name='program_student_degree_major_uc'),)
    

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

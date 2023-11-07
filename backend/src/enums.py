""" Class to store any enumerations used in models and main.py 
for data validation for certain data"""
import enum 

class DegreeLevels(str, enum.Enum):
    """Valid values for degree levels.
    """
    REGULAR_MASTERS = "Regular Masters"
    DOCTORAL = "Doctoral"
    PROVISIONAL_MASTERS = "Provisional Masters"
    REGULAR_POST_MASTERS = "Regular Post Masters"

class CourseType(str, enum.Enum):
    """Valid values for if the course is transfer or not From Course Enrollment.
    """
    TRANSFER = "Transfer"
    NOT_TRANSFER = "Non-Transfer"
       
    
class EventStatus(enum.Enum):
    """Valid values for status of event.
    """
    ON_GOING = 1
    COMPLETE = 2
    
class AdvisorRole(enum.Enum):
    """Valid values for Advisor Role.
    """
    MAIN_ADVISOR = 1
    CO_ADVISOR = 2
    
    
class Residencies(str, enum.Enum):
    """Values that are valid for residencies of student.
    """
    IN_STATE = "in_state"
    OUT_OF_STATE = "out_of_state"
    
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
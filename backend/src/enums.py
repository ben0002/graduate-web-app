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
       
    
class EventStatus(str, enum.Enum):
    """Valid values for status of event.
    """
    ON_GOING = "on_going"
    COMPLETE = "complete"
    
class AdvisorRole(str, enum.Enum):
    """Valid values for Advisor Role.
    """
    MAIN_ADVISOR = "main_advisor"
    CO_ADVISOR = "co_advisor"
    
    
class Residencies(str, enum.Enum): # should we make va_residency true and false or keep the enums?
    """Values that are valid for residencies of student.
    """
    IN_STATE = "In-State"
    OUT_OF_STATE = "Out-of-State"
    
class StudentStatus(str, enum.Enum): # need to ask the difference b/n status and type bc can student set status in their pfp?
    """Values that are valid for student status'.
    """
    STATUS_1 = 1
    STATUS_2 = 2
    STATUS_3 = 3

class AdmitType(str, enum.Enum): # do we get rid of admit type?
    """Values that are valid for admission types of students.
    """
    ADMIT_1 = 1
    ADMIT_2 = 2
    ADMIT_3 = 3

class StudentTypes(str, enum.Enum): # ask question about this in relation to student status 
    """Values that are valid for the different student types.
    """
    NEW = "new"
    CONT = "continuing"
    NEW_PROGRAM = "new_program"
""" Class to store any enumerations used in models and main.py 
for data validation for certain data"""
import enum 
       
    
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
    

class StudentStatus(str, enum.Enum): # ask question about this in relation to student status 
    """Values that are valid for the different student types.
    """
    NEW = "New"
    CONT = "Cont"
    NEW_PROGRAM = "New Prog"
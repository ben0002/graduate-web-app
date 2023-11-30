from sqlalchemy.orm import Session
import models
from io import TextIOWrapper
from fastapi import UploadFile
from pydantic import EmailStr
from datetime import datetime
import schemas
import models
import enums
import csv
import re

class CustomException(Exception):
    def __init__(self, message, original_exception, row_data=None):
        super().__init__(message)
        self.row_data = row_data
        self.original_exception = original_exception
    def set_row(self, row):
        self.row_data = row
        
class CustomValueError(CustomException):
    pass

def apply_filters(query,  model, filters: dict = {}):
    """
    Apply filters to a SQLAlchemy query based on the specified model and filter criteria.

    Parameters:
    - query (sqlalchemy.orm.query.Query): The SQLAlchemy query to be filtered.
    - model (sqlalchemy.ext.declarative.DeclarativeMeta): The SQLAlchemy model representing the database table.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.

    Returns:
    - sqlalchemy.orm.query.Query: The filtered SQLAlchemy query.
    """
    if filters is None:
        return query
    
    for attr,value in filters.items():
        if value is not None:
            query = query.filter( getattr(model,attr)==value )
    return query

def get_students(db: Session, filters: dict, skip: int = 0, limit: int =100):
    """
    Retrieve a list of students based on the Student model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing students
    """
    query = db.query(models.Student)
    query = apply_filters(query, models.Student, filters)
    #if(filters.get("citizenship", None) is not None):
        #query = query.filter(models.Student.visa["citizenship"] == filters.get("citizenship"))
    return query.offset(skip).limit(limit).all()

def get_faculty(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of facultys based on the faculty model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing faculty
    """
    query = db.query(models.Faculty)
    query = apply_filters(query, models.Faculty, filters)
    
    return query.offset(skip).limit(limit).all()

def get_degrees(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of degrees based on the degree model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing degree 
    """
    query = db.query(models.Degree)
    query = apply_filters(query, models.Degree, filters)
    
    return query.offset(skip).limit(limit).all()

def get_majors(db: Session, filters, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of majors based on the major model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing major
    """
    query = db.query(models.Major)
    query = apply_filters(query, models.Major, filters)
    
    return query.offset(skip).limit(limit).all()

def get_messages(db: Session, filters, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of messages based on the message model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing message
    """
    query = db.query(models.Message)
    query = apply_filters(query, models.Major, filters)
    
    return query.offset(skip).limit(limit).all()

def get_campus(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of campus based on the campus model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing campus
    """
    query = db.query(models.Campus)
    query = apply_filters(query, models.Campus, filters)
    
    return query.offset(skip).limit(limit).all()

def get_department(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of department based on the department model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing department
    """
    query = db.query(models.Department)
    query = apply_filters(query, models.Department, filters)
    
    return query.offset(skip).limit(limit).all()

def get_programEnrollment(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of program enrollment based on the ProgramEnrollment model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing program enrollment
    """
    query = db.query(models.ProgramEnrollment)
    query = apply_filters(query, models.ProgramEnrollment, filters)
    
    return query.offset(skip).limit(limit).all()

def get_studentLab(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student lab based on the StudentLabs model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing student lab
    """
    query = db.query(models.StudentLabs)
    query = apply_filters(query, models.StudentLabs, filters)
    
    return query.offset(skip).limit(limit).all()

def get_studentAdvisor(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student advisor based on the StudentAdvisor model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing student advisor
    """
    query = db.query(models.StudentAdvisor)
    query = apply_filters(query, models.StudentAdvisor, filters)
    
    return query.offset(skip).limit(limit).all()

def get_employment(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student's employment based on the employment model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing employment
    """
    query = db.query(models.Employment)
    query = apply_filters(query, models.Employment, filters)
    
    return query.offset(skip).limit(limit).all()

def get_funding(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student's funding based on the funding model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing funding
    """
    query = db.query(models.Funding)
    query = apply_filters(query, models.Funding, filters)
    
    return query.offset(skip).limit(limit).all()

def get_event(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student's event based on the event model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing event
    """
    query = db.query(models.Event)
    query = apply_filters(query, models.Event, filters)
    
    return query.offset(skip).limit(limit).all()


def get_requirement(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of requirement based on the requirement model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing requirement
    """
    query = db.query(models.Requirement)
    query = apply_filters(query, models.Requirement, filters)
    
    return query.offset(skip).limit(limit).all()

def get_milestone(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of milestone based on the milestone model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing milestone
    """
    query = db.query(models.Milestone)
    query = apply_filters(query, models.Milestone, filters)
    
    return query.offset(skip).limit(limit).all()

def get_progress(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student's progress based on the progress model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing progress
    """
    query = db.query(models.Progress)
    query = apply_filters(query, models.Progress, filters)
    
    return query.offset(skip).limit(limit).all()

def get_courseEnrollment(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student's course enrollment based on the CourseEnrollment model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing course enrollment
    """
    query = db.query(models.CourseEnrollment)
    query = apply_filters(query, models.CourseEnrollment, filters)
    
    return query.offset(skip).limit(limit).all()

def get_stage(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student's stage based on the stage model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing stage
    """
    query = db.query(models.Stage)
    query = apply_filters(query, models.Stage, filters)
    
    return query.offset(skip).limit(limit).all()

def get_studentPOS(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of student's pos based on the StudentPOS model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing student's POS
    """
    query = db.query(models.StudentPOS)
    query = apply_filters(query, models.StudentPOS, filters)
    
    return query.offset(skip).limit(limit).all()

def delete_data(db: Session, filter: dict, model):
    """
    Delete data in database based on the specified model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - model (sqlalchemy.ext.declarative.DeclarativeMeta): The SQLAlchemy model representing the database table.
    
    Returns:
    - bool: True if the target data is found and deleted successfully, False otherwise.
    """
    try:
        query = db.query(model)
        query = apply_filters(query, model, filter).first()
        if query:
            db.delete(query)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        db.rollback()
        print(e)
    
def delete_requirement(db: Session, requirement_id: int):
    query = db.query(models.Requirement).filter(models.Requirement.id == requirement_id).one_or_none()
    if query:
        db.delete(query)
        db.flush()
        
        related_progress_entries = db.query(models.Progress).filter(models.Progress.requirement_id == requirement_id).all()
        for progress_entry in related_progress_entries:
            db.delete(progress_entry)
            db.flush()
    db.commit()

def delete_milestone(db: Session, milestone_id: int):
    query = db.query(models.Milestone).filter(models.Milestone.id == milestone_id).one_or_none()
    if query:
        db.delete(query)
        db.flush()
        
        related_progress_entries = db.query(models.Progress).filter(models.Progress.milestone_id == milestone_id).all()
        for progress_entry in related_progress_entries:
            db.delete(progress_entry)
            db.flush()
    db.commit()

def delete_program_enrollment(db:Session, program_id: int):
    
    # delete program
    program = db.query(models.ProgramEnrollment).filter(models.ProgramEnrollment.id == program_id).one()
    db.delete(program)
    db.flush()
    # delete all progress with major.id and degree.id and student.id
    
    # grab all requirements with that major.id and degree.id
    related_reqs = db.query(models.Requirement).filter(models.Requirement.major_id == program.major_id,
                                                         models.Requirement.degree_id == program.degree_id).all()
    

    # query progress to get progress with related requirement.id and delete
    for req in related_reqs:
        progress = db.query(models.Progress).filter(models.Progress.requirement_id == req.id, 
                                                    models.Progress.student_id == program.student_id).one_or_none()
        db.delete(progress)
        db.flush()
    
    # delete all milestones with major.id and degree.id
    related_milestones = db.query(models.Milestone).filter(models.Milestone.major_id == program.major_id,
                                                         models.Milestone.degree_id == program.degree_id).all()
    for milestone in related_milestones:
        progress = db.query(models.Progress).filter(models.Progress.milestone_id == milestone.id, 
                                                    models.Progress.student_id == program.student_id).one_or_none()
        db.delete(progress)
        db.flush()
        
    db.commit()
    
def update_data(db: Session, filter: dict, model, data):
    """
    Update data in database based on the specified model, filter criteria, and input data. It will only update
    the data that is not none. none means user did not input.
    
    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - model (sqlalchemy.ext.declarative.DeclarativeMeta): The SQLAlchemy model representing the database table.
    - data (schema): it is input data passed by schema request body
    
    Returns:
    - sqlalchemy.ext.declarative.DeclarativeMeta: The updated data after applying changes.
    """
    query = db.query(model)
    query = apply_filters(query, model, filter).first()
    if not query:
        raise CustomValueError(message="The given id is not found in the Database.", original_exception=None, row_data=1)
    for field, value in data.dict(exclude_unset=True, exclude={'student_id'}).items():
            if value is not None:
                setattr(query, field, value)
    db.commit()
    db.refresh(query)
    return query

def update_requirement(db: Session, requirement_id: int, data:schemas.RequirementPatch):
    
    update_dict = data.dict(exclude_unset=True)
    db.query(models.Requirement).filter(models.Requirement.id == requirement_id).update(update_dict)
    db.commit()     
    return  db.query(models.Requirement).filter(models.Requirement.id == requirement_id).one()


def update_milestone(db: Session, milestone_id: int, data:schemas.MilestonePatch):
    
    update_dict = data.dict(exclude_unset=True)
    db.query(models.Milestone).filter(models.Milestone.id == milestone_id).update(update_dict)
    db.commit()     
    return  db.query(models.Milestone).filter(models.Milestone.id == milestone_id).one()

def update_progress_data(db: Session, filter: dict, model, data):
    """
    Update progress data in database based on the specified model, filter criteria, and input data. It will only update
    the data that is not none. none means user did not input.
    
    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - model (sqlalchemy.ext.declarative.DeclarativeMeta): The SQLAlchemy model representing the database table.
    - data (schema): it is input data passed by schema request body
    
    Returns:
    - sqlalchemy.ext.declarative.DeclarativeMeta: The updated data after applying changes.
    """
    query = db.query(model)
    query = apply_filters(query, model, filter).first()
    if not query:
        raise CustomValueError(message="The given id is not found in the Database.", original_exception=None, row_data=1)
    if (data.custom_milestone_name is not None or data.custom_milestone_description is not None) and (query.requirement_id is not None or query.milestone_id is not None):
        raise CustomValueError(message="The given id is not validated because it cannot modify the custom_milestone_name while having requirement and milestone.", original_exception=None, row_data=1)
    for field, value in data.dict(exclude_unset=True, exclude={'student_id'}).items():
            if value is not None:
                setattr(query, field, value)
    db.commit()
    db.refresh(query)
    return query
    
    

def update_programenrollment_data(db: Session, filter: dict, model, data):
    """
    Update data in database based on the specified model, filter criteria, and input data.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - model (sqlalchemy.ext.declarative.DeclarativeMeta): The SQLAlchemy model representing the database table.
    - data (schema): it is input data passed by schema request body
    
    Returns:
    - sqlalchemy.ext.declarative.DeclarativeMeta: The updated data after applying changes.
    """
    programenrollment = db.query(model)
    programenrollment = apply_filters(programenrollment, model, filter).first()
    if not programenrollment:
        raise CustomValueError(message="The given id is not found in the Database.", original_exception=None, row_data=1)
    #If the major or degre is changed, we will need to delete the original progress that related to the degree and major. And add the new one with the new degree and major id.
    delete_progress(programenrollment, db)
   
    for field, value in data.dict(exclude_unset=True, exclude={'student_id'}).items():
            if value is not None:
                setattr(programenrollment, field, value)
    db.flush()
    # making a new progress
    filter_temp = {
        "degree_id" : programenrollment.degree_id,
        "major_id" : programenrollment.major_id
    }
    milestones = db.query(models.Milestone)
    milestones = apply_filters(milestones, models.Milestone, filter_temp).all()
    requirements= db.query(models.Requirement)
    requirements = apply_filters(requirements, models.Requirement, filter_temp).all()
    
    for milestone in milestones:
        milestone_progress = schemas.ProgressIn(
            milestone_id=milestone.id,
            student_id=programenrollment.student_id
        )
        milestone_db = models.Progress(**milestone_progress.dict())
        db.add(milestone_db)
        db.flush()
    
    for requirement in requirements:
        requirement_progress = schemas.ProgressIn(
            requirement_id=requirement.id,
            student_id=programenrollment.id
        )
        requirement_db= models.Progress(**requirement_progress.dict())
        db.add(requirement_db)
        db.flush()
        
    db.commit()
    db.refresh(programenrollment)
    return programenrollment

def delete_progress(programenrollment, db: Session):
    """
    Retrieve a list of student's event based on the event model and filter criteria.

    Parameters:
    - db (Session): the database session.
    - filters (dict, optional): A dictionary containing filter criteria where keys represent model attributes
      and values represent desired attribute values. Defaults to an empty dictionary.
    - skip (int, optional): The number of records to skip. Defaults to 0.
    - limit (int, optional): The maximum number of records to return. Defaults to 100.
    
    Returns:
    - List[sqlalchemy.ext.declarative.DeclarativeMeta]: A list of SQLAlchemy model instances representing event
    """
    related_reqs = db.query(models.Requirement).filter(models.Requirement.major_id == programenrollment.major_id,
                                                         models.Requirement.degree_id == programenrollment.degree_id).all()
    for req in related_reqs:
        progress = db.query(models.Progress).filter(models.Progress.requirement_id == req.id, 
                                                    models.Progress.student_id == programenrollment.student_id).one_or_none()
        db.delete(progress)
        db.flush()
    
    related_milestones = db.query(models.Milestone).filter(models.Milestone.major_id == programenrollment.major_id,
                                                         models.Milestone.degree_id == programenrollment.degree_id).all()
    for milestone in related_milestones:
        progress = db.query(models.Progress).filter(models.Progress.milestone_id == milestone.id, 
                                                    models.Progress.student_id == programenrollment.student_id).one_or_none()
        db.delete(progress)
        db.flush()
    
    db.commit()
            
def check_either_one(data):
    if data.milestone_id is None and data.requirement_id is None:
        return True
    if data.custom_milestone_name is None and data.requirement_id is None:
        return True
    if data.custom_milestone_name is None and data.milestone_id is None:
        return True
    return False

#--------------------------------------------------Insert Data Function For File-------------------------

def insert_requirement(requirement: schemas.RequirementIn, db:Session):
    
    db_requirement = models.Requirement(**requirement.dict())
    db.add(db_requirement)
    db.flush()
    requirement_id = db_requirement.id
    programEnrollments = db.query(models.ProgramEnrollment).filter(models.ProgramEnrollment.degree_id==requirement.degree_id, 
                                                                models.ProgramEnrollment.major_id==requirement.major_id).all()
    for programEnrollment in programEnrollments:
        progress_data = schemas.ProgressIn(
            student_id=programEnrollment.student_id,
            requirement_id=requirement_id,              
        )
        progress_data.deadline = "TBD"
        progress = models.Progress(**progress_data.dict())
        db.add(progress)
        db.flush()
        
    db.commit()
    return requirement

def insert_milestone(milestone: schemas.MilestoneIn, db:Session):
    
    db_milestone = models.Milestone(**milestone.dict())
    db.add(db_milestone)
    db.flush()
    milestone_id = db_milestone.id
    programEnrollments = db.query(models.ProgramEnrollment).filter(models.ProgramEnrollment.degree_id==milestone.degree_id, 
                                                                models.ProgramEnrollment.major_id==milestone.major_id).all()
    for programEnrollment in programEnrollments:
        progress_data = schemas.ProgressIn(
            student_id=programEnrollment.student_id,
            milestone_id=milestone_id,              
        )
        progress_data.deadline="TBD"
        progress = models.Progress(**progress_data.dict())
        db.add(progress)
        db.flush()
        
    db.commit()
    return milestone
# Processing data from file to StudentPOS table
def insert_student_pos_from_file(data : dict, db: Session, student_id: int):
    # checking if it is approved, none mean it has not been approved yet
    approved = False
    if not data.get("POS Approved"):
        approved = True
    student_pos = models.StudentPOS(
        approved = approved,
        approved_date = data.get("POS Approved") or None,
        chair = data.get("POS Chair") or None,
        co_chair = data.get("POS CoChair") or None,
        student_id = student_id
    )
    db.add(student_pos)
    db.commit()
    # Since no table need the primary id from Student POS currently, it does not return the id.
    # Feel free to reutrn id if it needs
    
# Processing data from file to Student table

# it is on the calling function to do db.commit()
def insert_student(data : dict, db: Session):
    student = models.Student(**data)
    db.add(student)
    db.flush()
    # This will return the primary id for ForeignKey that other table may need
    return student.id

def insert_student_advisor_from_file(advisor_id: int, student_id: int, role: enums.AdvisorRole, db: Session,):
    student_advisor = models.StudentAdvisor(
        advisor_id = advisor_id,
        student_id = student_id,
        advisor_role = role
    )
    db.add(student_advisor)
    db.flush()

def insert_program_enrollment(program: schemas.ProgramEnrollmentIn, db: Session):
    
    programEnrollment = models.ProgramEnrollment(
            student_id = program.student_id,
            degree_id = program.degree_id,
            major_id = program.major_id,
            enrollment_date = program.enrollment_date
    )
    
    db.add(programEnrollment)
    
    requirements = get_requirement(db=db, filters={"major_id": program.major_id, "degree_id": program.degree_id})
    
    for requirement in requirements:
        progress = models.Progress(
            student_id=program.student_id,
            requirement_id=requirement.id,
            deadline="TBD",
            approved=False,
            exempt=False   
        )
        db.add(progress)
    
    milestones = get_milestone(db=db, filters={"major_id": program.major_id, "degree_id": program.degree_id})
    
    for milestone in milestones:
        progress = models.Progress(
            student_id=program.student_id,
            milestone_id=milestone.id,
            deadline="TBD",
            approved=False,
            exempt=False   
        )
        db.add(progress)
        
    db.flush()
    
    
# Processing data from file to ProgramEnrollment table
def insert_program_enrollment_from_file(data : dict, db: Session, student_id: int, degree_id: int, major_id: int):
    # make sure do not have duplicate table
    programEnrollment = db.query(models.ProgramEnrollment).filter(models.ProgramEnrollment.degree_id == degree_id, models.ProgramEnrollment.student_id == student_id, models.ProgramEnrollment.major_id == major_id).one_or_none()
    if not programEnrollment:
        
        validation = schemas.ProgramEnrollmentFileIn(
            student_id=student_id,
            degree_id=degree_id,
            major_id=major_id,
            enrollment_date="30-MAR-23" #this is defualt value Since we don't have the data about enrollment_date
        )

        programEnrollment = models.ProgramEnrollment(
            student_id = validation.student_id,
            degree_id = validation.degree_id,
            major_id = validation.major_id,
            enrollment_date = validation.enrollment_date
        )
        db.add(programEnrollment)
        db.flush()
        
# Processing data from file to Campus table
def insert_campus_from_file(data: dict, db: Session):
    campus_name = data.get("name") #it does not have campus name, so I use the ID number indicate the name.
    # This will check if the table with the same campus name is exist.
    # It is to avoid duplicated table
    campus = db.query(models.Campus).filter(models.Campus.name == campus_name).one_or_none()
    if not campus:
        campus = models.Campus(**data)
        db.add(campus)
        db.flush()

# Processing data from file to Department table.
# These inserted value below is non-real data, and it is for testing.
def insert_department_from_file(data : dict, db: Session):
    department = db.query(models.Department).filter(models.Department.name == data.get("name")).one_or_none()
    # This will check if the table with the same department name is exist.
    # It is to avoid duplicated table
    if not department:
        department = models.Department(**data)
        db.add(department)
        db.flush()

# Processing data from file to Major table
def insert_major_from_file(data : dict, db: Session):
    major_name = data.get("name")
    # This will check if the table with the same major name is exist.
    # It is to avoid duplicated table
    major = db.query(models.Major).filter(models.Major.name == major_name).one_or_none()
    if not major:
        major = models.Major(**data)
        db.add(major)
        db.flush()
        
# Processing data from file to Degree table
def insert_degree_from_file(data : dict, db: Session):
    degree_name = data.get("name")
    degree = db.query(models.Degree).filter(models.Degree.name == degree_name).one_or_none()
    if not degree:
        # Modeling the field with the data from file
        degree = models.Degree(**data)  
        db.add(degree)
        db.flush()
        
# Processing data from file to Faculty table
def insert_faculty_from_file(data : dict, db: Session):
    # Modeling the field with the data from file
    faculty = models.Faculty(**data)  
    db.add(faculty)
    db.flush()

# Processing data from file to Milestone table
def insert_milestone_from_file(data : schemas.MilestoneIn, db: Session):
    # Modeling the field with the data from file
    insert_milestone(data, db)
    
# Processing data from file to Requirement table
def insert_requirement_from_file(data : schemas.RequirementIn, db: Session):
    # Modeling the field with the data from file
    insert_requirement(data, db)
#------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------Helper function for validation--------------------------------------------
#this will return the campus id corresponding to campus name. However, if the campus is not exist, it will thrown error excpetion
def find_campus(campus_name: str, db: Session, row_number: int):
    #if the campus is none, then return none for the id
    if not campus_name:
        return None
    campus = db.query(models.Campus).filter(models.Campus.name == campus_name).first()
    if campus:
        return campus.id
    else:
        raise CustomValueError(message="The campus \"" + campus_name + "\" is not found in the Database.", original_exception=None, row_data=row_number)
        
def find_advisor(advisor_name: str, db:Session, row_number: int):
    if not advisor_name:
        return None
    last_name, first_name = map(str.strip, advisor_name.split(',', 1))
    advisor = db.query(models.Faculty).filter(models.Faculty.last_name == last_name, models.Faculty.first_name == first_name).first()
    if advisor:
        return advisor.id
    else:
        raise CustomValueError(message="The advisor \"" + advisor_name + "\" is not found in the Database.", original_exception=None, row_data=row_number)

def find_co_advisor(advisor_name: str, db:Session, row_number: int):
    if not advisor_name:
        return None
    list_name = re.split(r'\s{2,}', advisor_name)
    advisor_id = []
    for name in list_name:
        last_name, first_name = map(str.strip, name.split(',', 1))
        advisor = db.query(models.Faculty).filter(models.Faculty.last_name == last_name, models.Faculty.first_name == first_name).first()
        if advisor:
            advisor_id.append(advisor.id)
        else:
            raise CustomValueError(message="The advisor \"" + advisor_name + "\" is not found in the Database.", original_exception=None, row_data=row_number)
    return advisor_id
    
# This will find degree and return degree id. 
def find_degree(degree_name: str, db: Session, row_number: int):
    if not degree_name:
        raise CustomValueError(message="The degree is need.", original_exception=None)
    degree = db.query(models.Degree).filter(models.Degree.name == degree_name).one_or_none()
    if degree:
        return degree.id
    else:
        raise CustomValueError(message="The degree \"" + degree_name + "\" is not found in the Database.", original_exception=None, row_data=row_number)
# This will find major and return the id itself 
def find_major(db: Session, row_number: int, major_description: str = None, major_name: str = None, ):
    
    major = None
    if major_description:
        major = db.query(models.Major).filter(models.Major.description == major_description).one_or_none()
    elif major_name: 
        major = db.query(models.Major).filter(models.Major.name == major_name).one_or_none()
        
    if not major_description and not major_name:
        raise CustomValueError(message="The major is need.", original_exception=None)
   
    if major:
        return major.id
    elif major_description:
        raise CustomValueError(message="The major \"" + major_description + "\" is not found in the Database.", original_exception=None, row_data=row_number)
    else:
        raise CustomValueError(message="The major \"" + major_name + "\" is not found in the Database.", original_exception=None, row_data=row_number)
        

# This will find major with its name and return the id itself 
def find_major_name(major_name: str, db: Session, row_number: int):
    if not major_name:
        raise CustomValueError(message="The given major name + " + major_name + "is not found.", original_exception=None, row_data=row_number)
    major = db.query(models.Major).filter(models.Major.name == major_name).one_or_none()
    if major:
        return major.id
    else:
        raise CustomValueError(message="The major \"" + major_name + "\" is not found in the Database.", original_exception=None, row_data=row_number)

# This will find department and return the id itself 
def find_department(department_name: str, db: Session, row_number: int):
    # Not sure if it can be none
    if not department_name:
        return None
    department = db.query(models.Department).filter(models.Department.name == department_name).one_or_none()
    if department:
        return department.dept_code
    else:
        raise CustomValueError(message="The department \"" + department_name + "\" is not found in the Database.", original_exception=None, row_data=row_number)

# This will find student pos and return the id itself 
def find_studentpos(student_id: int, db: Session):
    # Not sure if it can be none
    if not student_id:
        raise CustomValueError(message="The student id is need.", original_exception=None)
    studentpos = db.query(models.StudentPOS).filter(models.StudentPOS.student_id == student_id).one_or_none()
    if studentpos:
        return studentpos.id
    else:
        return None
    
#--------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------Validation Function--------------------------------------------
# This will help to validate the data from csv file when insert the data for student
def validation_student_data_from_file(data: dict, db: Session, row_number: int):
    degree_id = find_degree(data.get("Degree") or None, db, row_number)
    major_id = find_major(major_description=data.get("Major") or None, db=db, row_number=row_number)
    advisor_id = find_advisor(data.get("Advisor") or None, db, row_number)
    co_advisor_id = find_co_advisor(data.get("Co-Advisor") or None, db, row_number)
    validation_data = schemas.StudentFileUpload(
        first_name = data.get("First/Middle Name") or None,
        pronouns= data.get("Preferred Pronouns") or None,
        last_name = data.get("Last Name") or None,
        campus_id = find_campus(data.get("Campus") or None, db, row_number),
        va_residency = enums.Residencies(data.get("Virginia Residency")) or None,
        status = enums.StudentStatus(data.get("Student Status")) or None,
        email = data.get("E-mail") or None,
        phone_number = data.get("Phone") or None,
        citizenship = data.get("Country of Citizenship") or None,
        advisory_committee = data.get("Advisory Committee") or None,
        plan_submit_date = data.get("Plan Submitted") or None,
        prelim_exam_pass = data.get("Prelim Exam Passed") or None,
        proposal_meeting = data.get("Proposal Meeting") or None,
        progress_meeting = data.get("Progress Meeting") or None,
        final_exam = data.get("Final Exam") or None,
        enrollment_term=enums.AcademicTerm(data.get("Enrollment Term")) if data.get("Enrollment Term") is not None else None,
        enrollment_year=data.get("Enrollment Year", None),
        ETD_submitted = data.get("ETD Submitted") or None
    )
    return validation_data, degree_id, major_id, advisor_id, co_advisor_id
# This will help to validate the data from csv file when insert the data for campus
def validation_campus_data_from_file(data: dict, db:Session, row_number: int):
    validation_data = schemas.CampusIn(
        name = data.get("Campus Name"),
        address = data.get("Address") or None
    )
    return validation_data

# This will help to validate the data from csv file when insert the data for department
def validation_department_data_from_file(data: dict, db:Session, row_number: int):
    validation_data = schemas.DepartmentIn(
        name = data.get("department name") or None
    )
    return validation_data

# This will help to validate the data from csv file when insert the data for major
def validation_major_data_from_file(data: dict, db:Session, row_number: int):
    validation_data = schemas.MajorIn(
        dept_code = find_department(data.get("department name") or None, db, row_number),
        name = data.get("Majors") or None,
        description = data.get("description") or None
    )
    return validation_data

# This will help to validate the data from csv file when insert the data for degree
def validation_degree_data_from_file(data: dict, db:Session, row_number: int):
    validation_data = schemas.DegreeIn(
        name = data.get("Degrees") or None,
        description = data.get("description") or None
    )
    return validation_data

# This will help to validate the data from csv file when insert the data for degree
def validation_faculty_data_from_file(data: dict, db:Session, row_number: int):
    last_name, first_name = map(str.strip, data.get("Faculty name").split(',', 1))
    validation_data = schemas.FacultyIn(
        dept_code = find_department(data.get("department") or None, db, row_number),
        last_name = last_name or None,
        first_name = first_name or None,
        faculty_type = data.get("faculty type") or None,
        privilege_level = data.get("privilege level") or None,
        email= data.get("Email")
    )
    return validation_data

# This will help to validate the data from csv file when insert the data for degree
def validation_milestone_data_from_file(data: dict, db:Session, row_number: int):
    major_id = find_major_name(data.get("Major"), db, row_number)
    degree_id = find_degree(data.get("Degree"), db, row_number)
    validation_data = schemas.MilestoneIn(
        name=data.get("Name"),
        description=data.get("Description"),
        major_id=major_id,
        degree_id=degree_id
    )
    return validation_data

# This will help to validate the data from csv file when insert the data for degree
def validation_requirement_data_from_file(data: dict, db:Session, row_number: int):
    major_id = find_major_name(data.get("Major"), db, row_number)
    degree_id = find_degree(data.get("Degree"), db, row_number)
    validation_data = schemas.RequirementIn(
        name=data.get("Name"),
        description=data.get("Description"),
        major_id=major_id,
        degree_id=degree_id
    )
    return validation_data
#----------------------------------------------------------------------------------------------------------------------

#--------------------------------------------File Upload EndPoint Helper Function--------------------------------------------
# This will process student data from csv file, and add them to the corresponding database.
def process_student_data_from_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_student_data : list = []
        number_row = 1
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            validation_data, degree_id, major_id, advisor_id, co_advisor_id = validation_student_data_from_file(row, db, number_row)
            inserted_student_data.append(validation_data)
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            student_id = insert_student(dict(validation_data), db)
            insert_program_enrollment_from_file(row, db, student_id, degree_id, major_id)
            # make sure the advisor_id is not null
            if advisor_id:
                insert_student_advisor_from_file(advisor_id=advisor_id, student_id=student_id, role=enums.AdvisorRole.MAIN_ADVISOR, db=db)
            if co_advisor_id:
                for id in co_advisor_id:
                    insert_student_advisor_from_file(advisor_id=id, student_id=student_id, role=enums.AdvisorRole.CO_ADVISOR, db=db)
            #-----------------------------------------------------------------
            number_row += 1
        db.commit()
    return inserted_student_data


# This will process campus data from csv file, and add them to the corresponding database.
def process_campus_data_from_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_campus_data : list = []
        number_row = 1
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            validation_data = validation_campus_data_from_file(row, db, number_row)
            inserted_campus_data.append(validation_data)
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            insert_campus_from_file(dict(validation_data), db)
            #-----------------------------------------------------------------
            number_row += 1
        db.commit()
    return inserted_campus_data

# This will process department data from csv file, and add them to the corresponding database.
def process_department_data_from_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_department_data : list = []
        number_row = 1
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            validation_data = validation_department_data_from_file(row, db, number_row)
            inserted_department_data.append(validation_data)
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            insert_department_from_file(dict(validation_data), db)
            #-----------------------------------------------------------------
            number_row += 1
        db.commit()
    return inserted_department_data

# This will process major data from csv file, and add them to the corresponding database.
def process_major_data_from_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_major_data : list = []
        number_row = 1
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            validation_data = validation_major_data_from_file(row, db, number_row)
            inserted_major_data.append(validation_data)
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            insert_major_from_file(dict(validation_data), db)
            #-----------------------------------------------------------------
            number_row += 1
        db.commit()
    return inserted_major_data

# This will process major data from csv file, and add them to the corresponding database.
def process_degree_data_from_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_degree_data : list = []
        number_row = 1
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            validation_data = validation_degree_data_from_file(row, db, number_row)
            inserted_degree_data.append(validation_data)
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            insert_degree_from_file(dict(validation_data), db)
            #-----------------------------------------------------------------
            number_row += 1
        db.commit()
    return inserted_degree_data

# This will process major data from csv file, and add them to the corresponding database.
def process_faculty_data_from_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_faculty_data : list = []
        number_row = 1
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            validation_data = validation_faculty_data_from_file(row, db, number_row)
            inserted_faculty_data.append(validation_data)
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            insert_faculty_from_file(dict(validation_data), db)
            #-----------------------------------------------------------------
            number_row += 1
        db.commit()
    return inserted_faculty_data

# This will process milestone data from csv file, and add them to the corresponding database.
def process_milestone_data_from_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_milestone_data : list = []
        number_row = 1
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            validation_data = validation_milestone_data_from_file(row, db, number_row)
            inserted_milestone_data.append(validation_data)
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            insert_milestone_from_file(validation_data, db)
            #-----------------------------------------------------------------
            number_row += 1
        db.commit()
    return inserted_milestone_data

# This will process requirement data from csv file, and add them to the corresponding database.
def process_requirement_data_from_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_requirement_data : list = []
        number_row = 1
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            validation_data = validation_requirement_data_from_file(row, db, number_row)
            inserted_requirement_data.append(validation_data)
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            insert_requirement_from_file(validation_data, db)
            #-----------------------------------------------------------------
            number_row += 1
        db.commit()
    return inserted_requirement_data

#------------------------------------------------------------------------------------------------------------------------------
            
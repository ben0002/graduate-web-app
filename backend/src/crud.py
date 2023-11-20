from sqlalchemy.orm import Session, InstrumentedAttribute
from io import TextIOWrapper
from fastapi import UploadFile
from pydantic import EmailStr
from datetime import date
import schemas
import models
import enums
import csv


def apply_filters(query,  model, filters: dict = {}):
    for column, value in filters.items():
        if isinstance(getattr(model, column, None), InstrumentedAttribute):
            query = query.filter(getattr(model, column) == value)
    return query

def get_students(db: Session, filters: dict, skip: int = 0, limit: int =100):
    query = db.query(models.Student)
    query = apply_filters(query, models.Student, filters)
    if(filters.get("citizenship", None) is not None):
        query = query.filter(models.Student.visa["citizenship"] == filters.get("citizenship"))
    return query.offset(skip).limit(limit).all()

def get_faculty(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    query = db.query(models.Faculty)
    query = apply_filters(query, filters, models.Faculty)
    
    return query.offset(skip).limit(limit).all()

# Processing data from file to Campus table
def insert_campus_from_file(data, db: Session):
    campus_name = data.get("Campus") #it does not have campus name, so I use the ID number indicate the name.
    # This will check if the table with the same campus name is exist.
    # It is to avoid duplicated table
    campus = db.query(models.Campus).filter(models.Campus.name == campus_name).one_or_none()
    if not campus:
        campus = models.Campus(
            name = campus_name,
            address = data.get("Admit Camp") or None
        )
        db.add(campus)
        db.commit()
    # Since the primary key will be generate after commit(), I need to search the database agian in order to get the primary id    
    # This will return the primary id for ForeignKey that other table may need
    return db.query(models.Campus).filter(models.Campus.name == campus.name).first().id

# Processing data from file to Degree table
def insert_degree_from_file(data : dict, db: Session):
    degree_name = data.get("Degree")
    degree_level = data.get("Level")
    degree = db.query(models.Degree).filter(models.Degree.name == degree_name, models.Degree.level == degree_level).one_or_none()
    if not degree:
        # Modeling the field with the data from file
        degree = models.Degree(
            level = enums.DegreeLevels(degree_level),
            name = degree_name 
        )  
        db.add(degree)
        db.commit()
    # Since the primary key will be generate after commit(), I need to search the database agian in order to get the primary id    
    # This will return the primary id for ForeignKey that other table may need
    return db.query(models.Degree).filter(models.Degree.name == degree_name, models.Degree.level == degree_level).first().id

# Processing data from file to Major table
def insert_major_from_file(data : dict, db: Session, department_code: int):
    major_name = data.get("Major")
    # This will check if the table with the same major name is exist.
    # It is to avoid duplicated table
    major = db.query(models.Major).filter(models.Major.name == major_name).one_or_none()
    if not major:
        major = models.Major(
            name = major_name or None,
            description = data.get("Major Description") or None,
            dept_code = department_code
        )
        db.add(major)
        db.commit()
    # Since the primary key will be generate after commit(), I need to search the database agian in order to get the primary id    
    # This will return the primary id for ForeignKey that other table may need
    return db.query(models.Major).filter(models.Major.name == major_name).first().id

# Processing data from file to Student table
def insert_student_from_file(data : dict, db: Session, campus_id: int):
    student = models.Student(
        last_name = data.get("Last Name") or None,   
        va_residency = enums.Residencies(data.get("Residency")) or None,
        first_name = data.get("First/Middle Name") or None,
        type = enums.StudentTypes(data.get("Stud Type")) or None,
        first_term = data.get("First Term Enrl") or None,
        email = data.get("E-mail") or None,
        phone_number = data.get("Phone") or None,
        gender = data.get("Gender") or None,
        ethnicity = data.get("Ethnicity") or None,
        prelim_exam_date = data.get("Prelim Exam Scheduled") or None,
        prelim_exam_pass = data.get("Prelim Exam Passed") or None,
        advisory_committee = data.get("Adviser Name") or None,
        campus_id = campus_id
    )
    db.add(student)
    db.commit()
    # Since the primary key will be generate after commit(), I need to search the database agian in order to get the primary id    
    # This will return the primary id for ForeignKey that other table may need
    return db.query(models.Student).filter(models.Student.email == student.email).first().id

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

# Processing data from file to ProgramEnrollment table
def insert_program_enrollment_from_file(data : dict, db: Session, student_id: int, degree_id: int, major_id: int):
    # make sure do not have duplicate table
    programEnrollment = db.query(models.ProgramEnrollment).filter(models.ProgramEnrollment.degree_id == degree_id, models.ProgramEnrollment.student_id == student_id, models.ProgramEnrollment.major_id == major_id).one_or_none()
    if not programEnrollment:
        programEnrollment = models.ProgramEnrollment(
            student_id = student_id,
            degree_id = degree_id,
            major_id = major_id,
            enrollment_date = "01-01-2023" #this is defualt value Since we don't have the data about enrollment_date
        )
    db.add(programEnrollment)
    db.commit()
    # Since no table need the primary id from ProgramEnrollment currently, it does not return the id.
    # Feel free to reutrn id if it needs

# Processing data from file to Visa table
def insert_visa_from_file(data : dict, db: Session, student_id: int):
    visa = models.Visa(
        citizenship = data.get("Country of Citizenship") or None,
        student_id = student_id
    )
    db.add(visa)
    db.commit()
    # Since no table need the primary id from Visa currently, it does not return the id.
    # Feel free to reutrn id if it needs

# Processing data from file to Department table.
# These inserted value below is non-real data, and it is for testing.
def insert_department_from_file(data : dict, db: Session):
    
    department = db.query(models.Department).filter(models.Department.name == "CS").one_or_none()
    # This will check if the table with the same department name is exist.
    # It is to avoid duplicated table
    if not department:
        department = models.Department(
            name="CS"
        )
        db.add(department)
        db.commit()
    # Since the primary key will be generate after commit(), I need to search the database agian in order to get the primary id    
    # This will return the primary id for ForeignKey that other table may need
    return db.query(models.Department).filter(models.Department.name == "CS").first().dept_code

def validation_data_from_file(data: dict):
    validation_data = schemas.FileUpload(
        first_name = data.get("First/Middle Name") or None,
        last_name = data.get("Last Name") or None,
        campus = data.get("Campus") or None,
        va_residency = enums.Residencies(data.get("Residency")) or None,
        type = enums.StudentTypes(data.get("Stud Type")) or None,
        admit_camp = data.get("Admit Camp") or None,
        level = enums.DegreeLevels(data.get("Level")) or None,
        degree_name = data.get("Degree") or None,
        major_name = data.get("Major") or None,
        major_description = data.get("Major Description") or None,
        first_term = data.get("First Term Enrl") or None,
        pos_approveddate = data.get("POS Approved") or None,
        pos_chair = data.get("POS Chair") or None,
        pos_co_chair = data.get("POS CoChair") or None,
        email = data.get("E-mail") or None,
        phone_number = data.get("Phone") or None,
        country_citizenship = data.get("Country of Citizenship") or None,
        gender = data.get("Gender") or None,
        ethnicity = data.get("Ethnicity") or None,
        advisory_committee = data.get("Adviser Name") or None,
        prelim_exam_date = data.get("Prelim Exam Scheduled") or None,
        prelim_exam_pass = data.get("Prelim Exam Passed") or None
    )
    return validation_data


# This will process data from csv file, and add them to the corresponding database.
def process_csv_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_student_data : list = []
        for row in csv_reader:
            #--------------Validation-----------------------------------------
            inserted_student_data.append(validation_data_from_file(row))
            #-----------------------------------------------------------------
            #----------------Insert To Database ------------------------------
            campus_id = insert_campus_from_file(row, db)
            degree_id = insert_degree_from_file(row, db)
            dept_code = insert_department_from_file(row, db)
            # it there is faculty, please do it below department
            major_id = insert_major_from_file(row, db, dept_code)# -1 indicated there is no department
            student_id = insert_student_from_file(row, db, campus_id)
            ##faculty = models.Faculty()
            ##student_advisor = models.StudentAdvisor()
            insert_student_pos_from_file(row, db, student_id)
            insert_program_enrollment_from_file(row, db, student_id, degree_id, major_id)
            insert_visa_from_file(row, db, student_id)
            #-----------------------------------------------------------------
    return inserted_student_data
            
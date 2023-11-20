from sqlalchemy.orm import Session, InstrumentedAttribute, joinedload
import models
from io import TextIOWrapper
import csv
from fastapi import UploadFile
import enums
from pydantic import EmailStr
from datetime import datetime

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
    if filters is None:
        return query
    
    for attr,value in filters.items():
        if value is not None:
            query = query.filter( getattr(model,attr)==value )
    return query

def get_students(db: Session, filters: dict, skip: int = 0, limit: int =100):
    query = db.query(models.Student)
    query = apply_filters(query, models.Student, filters)
    #if(filters.get("citizenship", None) is not None):
        #query = query.filter(models.Student.visa["citizenship"] == filters.get("citizenship"))
    return query.offset(skip).limit(limit).all()


def get_faculty(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    query = db.query(models.Faculty)
    query = apply_filters(query, models.Faculty, filters)
    
    return query.offset(skip).limit(limit).all()

def get_degrees(db: Session, filters: dict, skip: int = 0, limit: int = 100):
    query = db.query(models.Degree)
    query = apply_filters(query, models.Degree, filters)
    
    return query.offset(skip).limit(limit).all()

def get_majors(db: Session, filters, skip: int = 0, limit: int = 100):
    query = db.query(models.Major)
    query = apply_filters(query, models.Major, filters)
    
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
    degree = db.query(models.Degree).filter(models.Degree.name == degree_name).one_or_none()
    if not degree:
        # Modeling the field with the data from file
        degree = models.Degree(
            name = degree_name 
        )  
        db.add(degree)
        db.commit()
    # Since the primary key will be generate after commit(), I need to search the database agian in order to get the primary id    
    # This will return the primary id for ForeignKey that other table may need
    return db.query(models.Degree).filter(models.Degree.name == degree_name).first().id

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

def convert_to_date(date: str | None):
    
    date_format = "%d-%b-%y"
    if date == "" or date is None:
        return None
    try:
        # Attempt to convert the string to a date using the specified format
        date_object = datetime.strptime(date, date_format).date()
        return date_object
    except ValueError as ve:
        raise CustomValueError(message="Ensure the date given is in dd-month-yy (i.e. 05-APR-23) format for given row.",
                               original_exception=ve)

# Processing data from file to Student table
def insert_student_from_file(data : dict, db: Session, campus_id: int, response_data:list):
    
    #advisory_committee = data.get("Adviser Name") or None
    # formatting it as list
    #if isinstance(advisory_committee, str):
        #advisory_committee = [x.strip() for x in advisory_committee.split(",")]
    try:
        student = models.Student(
            last_name = data.get("Last Name") or None,   
            citizenship = data.get("Country of Citizenship"),
            va_residency = enums.Residencies(data.get("Residency")) or None,
            first_name = data.get("First/Middle Name") or None,
            type = enums.StudentTypes(data.get("Stud Type")) or None,
            first_term = data.get("First Term Enrl") or None,
            email = data.get("E-mail") or None,
            phone_number = data.get("Phone") or None,
            gender = data.get("Gender") or None,
            ethnicity = data.get("Ethnicity") or None,
            prelim_exam_date = convert_to_date(data.get("Prelim Exam Scheduled", None)),
            prelim_exam_pass = convert_to_date(data.get("Prelim Exam Passed", None)),
            advisory_committee = data.get("Adviser Name") or None,
            campus_id = campus_id
        )
        db.add(student)
        db.commit()
        table = db.query(models.Student).filter(models.Student.email == student.email).first()
        response_data.append(table.__dict__)
        # Since the primary key will be generate after commit(), I need to search the database agian in order to get the primary id    
        # This will return the primary id for ForeignKey that other table may need
        return table.id
    except CustomValueError as ve:
        raise 
    
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

# This will process data from csv file, and add them to the corresponding database.
def process_csv_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        inserted_student_data : list = []
        for row in csv_reader:
            try:
                campus_id = insert_campus_from_file(row, db)
                degree_id = insert_degree_from_file(row, db)
                dept_code = insert_department_from_file(row, db)
                # it there is faculty, please do it below department
                major_id = insert_major_from_file(row, db, dept_code)# -1 indicated there is no department
                student_id = insert_student_from_file(row, db, campus_id, inserted_student_data)
                ##faculty = models.Faculty()
                ##student_advisor = models.StudentAdvisor()
                insert_student_pos_from_file(row, db, student_id)
                insert_program_enrollment_from_file(row, db, student_id, degree_id, major_id)
            except CustomValueError as ve:
                ve.set_row(row)
                raise ve
    db.close()
    return inserted_student_data
            
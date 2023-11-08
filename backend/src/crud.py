from sqlalchemy.orm import Session, InstrumentedAttribute
import models
from io import TextIOWrapper
import csv
from fastapi import UploadFile
import enums


def apply_filters(query, filters: dict, model):
    for column, value in filters.items():
        if isinstance(getattr(model, column, None), InstrumentedAttribute):
            query = query.filter(getattr(model, column) == value)
    return query

def get_students(db: Session, filters: dict, skip: int = 0, limit: int =100):
    query = db.query(models.Student)
    query = apply_filters(query, filters, models.Student)
    return query.offset(skip).limit(limit).all()

def process_csv_file(file: UploadFile, db: Session):
    with TextIOWrapper(file.file, 'utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        
        for row in csv_reader:
            campus_name = row.get("Campus") #it does not have campus name, so I use the ID number indicate the name.
            campus = db.query(models.Campus).filter(models.Campus.name == campus_name).one_or_none()
            if not campus:
                campus = models.Campus(
                    name=campus_name,
                    address=row.get("Admit Camp")
                )
                
            degree_name = row.get("Degree")
            degree_level = row.get("Level")
            degree = db.query(models.Degree).filter(models.Degree.name == degree_name, models.Degree.level == degree_level).one_or_none()
            if not degree:
                degree = models.Degree(
                    level=enums.DegreeLevels(degree_level),
                    name=degree_name
                )
            
            major_name = row.get("Major")
            major = db.query(models.Major).filter(models.Major.name == major_name).one_or_none()
            if not major:
                major = models.Major(
                    name=major_name,
                    description=row.get("Major Description")
                    
                )
            
            visa = models.Visa(
                citizenship=row.get("Country of Citizenship")
            )
            
            student = models.Student(
                last_name=row.get("Last Name"),   
                va_residency=enums.Residencies(row.get("Residency")),
                first_name=row.get("First/Middle Name"),
                type=enums.StudentTypes(row.get("Stud Type")),
                first_term=row.get("First Term Enrl"),
                email=row.get("E-mail"),
                phone_number=row.get("Phone") 
            )
            
            
            
            
            db.close()
            return student, visa, major, degree, campus
            #db.add(instance_table)
                
        #db.commit()
        #db.close()
            
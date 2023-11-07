from sqlalchemy.orm import Session, InstrumentedAttribute
import models
from io import TextIOWrapper
import csv
from fastapi import UploadFile


def apply_filters(query, filters: dict, model):
    for column, value in filters.items():
        if isinstance(getattr(model, column, None), InstrumentedAttribute):
            query = query.filter(getattr(model, column) == value)
    return query

def get_students(db: Session, filters: dict, skip: int = 0, limit: int =100):
    query = db.query(models.Student)
    query = apply_filters(query, filters, models.Student)
    return query.offset(skip).limit(limit).all()

def process_csv_file(file: UploadFile, db: Session, Models):
    with TextIOWrapper(file.file, encoding='utf-8') as text_file:
        csv_reader = csv.DictReader(text_file)
        next(csv_reader)
            
        for row in csv_reader:
            instance_table = Models(**row)
            db.add(instance_table)
                
        db.commit()
        db.close()
            
from sqlalchemy.orm import Session, InstrumentedAttribute
import models


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
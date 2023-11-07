from sqlalchemy.orm import Session, InstrumentedAttribute
import models


def apply_filters(query, filters: dict, model):
    for column, value in filters.items():
        if isinstance(getattr(model, column, None), InstrumentedAttribute):
            query = query.filter(getattr(model, column) == value)
    return query

def get_students(db: Session, filters: dict, skip: int = 0, limit: int =100):
    query = db.query(models.Student)
    query = apply_filters(query, filters, models.Student)
    return query.offset(skip).limit(limit).all()


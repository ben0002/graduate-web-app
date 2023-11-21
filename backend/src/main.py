from fastapi import FastAPI, Depends, HTTPException, Request, Response, Cookie, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from sqlalchemy.orm import Session

from cas import CASClient

from enums import *
from datetime import date

import crud, schemas, models
from database import SessionLocal, engine

import csv

models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

origins = [
    "*",  # Example frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/")
def read_root():
    return {"message": "Hello, World!"}


SERVICE_URL = "https://bktp-gradpro.discovery.cs.vt.edu/"
SECRET_KEY = "03588c9b6f5508ff6ab7175ba9b38a4d1366581fdc6468e8323015db7d68dac0" # key used to sign JWT token
ALGORITHM = "HS256" # algorithm used to sign JWT Token
ACCESS_TOKEN_EXPIRE = 120

# Creating the CAS CLIENT
cas_client = CASClient(
    version=2,
    service_url=f"{SERVICE_URL}/api/login?",
    server_url="https://login.vt.edu/profile/cas/",
    # CHANGE: If you want VT CS CAS, to be used instead of VT CAS
    # change the server_url to https://login.cs.vt.edu/cas/
)

# Routes related to CAS
@app.get("/api/login")
def login(request: Request):

    username = request.cookies.get("username")
    if username: # return user info
        return {"message": "Logged in!"}

    cas_ticket = request.query_params.get("ticket")
    if not cas_ticket:
        cas_login_url = cas_client.get_login_url()
        return {"redirect_url": cas_login_url}

    (user, _, _) = cas_client.verify_ticket(cas_ticket)
    if not user:
        raise HTTPException(status_code=403, detail="Failed to verify ticket!")

    response = RedirectResponse(SERVICE_URL)
    response.set_cookie(key="username", value=user)
    return response

@app.get("/api/logout")
def logout(response: Response):
    cas_logout_url = cas_client.get_logout_url(SERVICE_URL)
    response.delete_cookie("username")
    return {"redirect_url": cas_logout_url}

#------------------- non-cas --------------------#

@app.get("/students", response_model=list[schemas.StudentOut])
def students(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
    admit_type: AdmitType | None = None, residency: Residencies | None = None, 
    student_type: StudentTypes | None = None, prelim_exam_date: date | None = None, 
    prelim_exam_passed: bool | None = None, first_term: int | None = None, 
    status: StudentStatus | None = None, campus_id: int | None = None 
):
    filters = {
        "admit_type": admit_type,
        "va_residency": residency,
        "student_type": student_type,
        "prelim_exam_date": prelim_exam_date,
        "prelim_exam_passed": prelim_exam_passed,
        "first_term": first_term,
        "status": status,
        "campus_id": campus_id,
    }   
    
    students = crud.get_students(db=db ,filters=filters, skip=skip, limit=limit)
    return students

# add filters once all basic func. is done
@app.get("/students/{student_id}", response_model=schemas.StudentOut)
async def students_id(student_id: int, db: Session = Depends(get_db)):
    filter = {
        "id": student_id
    }
    
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    return student[0]

@app.get("/faculty", response_model=list[schemas.FacultyOut])
async def faculty(
    skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db),
    dept_code: str | None = None, faculty_type: str | None = None,
    privilege_level: int | None = None):
    
    filters = {
        "dept_code": dept_code,
        "faculty_type": faculty_type.lower() if faculty_type is not None else None,
        "privilege_level": privilege_level
    }
    
    faculty = crud.get_faculty(db=db, filters=filters, skip=skip, limit=limit)
    return faculty

@app.get("/faculty/{faculty_id}", response_model=schemas.FacultyOut)
async def faculty_id(faculty_id: int, db: Session = Depends(get_db)):
    
    filter = {
        "id": faculty_id
    }
    faculty = crud.get_faculty(db=db, filters=filter)
    if(len(faculty) == 0):
        raise HTTPException(status_code=404, detail=f"Faculty member with the given id: {faculty_id} does not exist.")
    return faculty[0]


@app.get("/advisors", response_model=list[schemas.FacultyOut])
async def advisors(skip: int | None = 0, limit: int | None = 100, 
                   dept_code: str | None = None, privilege_level: int | None = None,
                   db: Session = Depends(get_db)):
    
    filters = {
        "faculty_type": "advisor",
        "dept_code": dept_code,
        "privilege_level": privilege_level
    }
    
    advisors = crud.get_faculty(db=db, filters=filters, skip=skip, limit=limit)
    return advisors

@app.get("/advisors/{advisor_id}", response_model=schemas.FacultyOut)
async def advisor(advisor_id: int, db: Session = Depends(get_db)):
        
    advisor = crud.get_faculty(db=db, filters={"id": advisor_id})
    if(len(advisor) == 0):
        raise HTTPException(status_code=404, detail=f"Advisor with the given id: {advisor_id} does not exist.")
    return advisor[0]
    
@app.get("/degrees", response_model=list[schemas.DegreeOut])
def degrees(db: Session = Depends(get_db), skip: int | None = 0, limit: int | None = 100):
    
    return crud.get_degrees(db, None, skip, limit)

@app.get("/degrees/{degree_id}", response_model=schemas.DegreeOut)
def degree(degree_id: int, db: Session = Depends(get_db)):
    
    filter = { "id": degree_id}
    
    degree = crud.get_degrees(db, filter, 0, 1)
    
    if(len(degree) == 0):
        raise HTTPException(status_code=404, detail=f"Degree with the given id: {degree_id} does not exist.")
    return degree[0]

@app.get("/majors", response_model=list[schemas.MajorOut])
def degrees(db: Session = Depends(get_db), skip: int | None = 0, limit: int | None = 100):
    
    return crud.get_majors(db, None, skip, limit)

@app.get("/majors/{major_id}", response_model=schemas.MajorOut)
def degree(major_id: int, db: Session = Depends(get_db), skip: int | None = 0, limit: int | None = 100):
    
    filters = {'id': major_id}
    
    major = crud.get_majors(db, filters, skip, limit)
    if(len(major) == 0):
        raise HTTPException(status_code=404, detail=f"Degree with the given id: {major_id} does not exist.")
    return major[0]



#---------------------------------File Upload EndPoint----------------------------------------
@app.post("/uploadstudentfile", response_model=list[schemas.StudentFileUpload])
async def upload_student_file(file: UploadFile, db: Session = Depends(get_db)):    
    try:
        return crud.process_student_data_from_file(file, db)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the CSV file")
    except csv.Error as csv_error:
        raise HTTPException(status_code=400, detail=f"CSV file error: {csv_error}")
    except ValueError as validation_error:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except crud.CustomValueError as value_error:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data}) 
    finally:
        db.close()
        
@app.post("/uploadcampusfile", response_model=list[schemas.CampusIn])
async def upload_campus_file(file: UploadFile, db: Session = Depends(get_db)):    
    try:
        return crud.process_campus_data_from_file(file, db)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the CSV file")
    except csv.Error as csv_error:
        raise HTTPException(status_code=400, detail=f"CSV file error: {csv_error}")
    except ValueError as validation_error:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except crud.CustomValueError as value_error:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data}) 
    finally:
        db.close()
        
@app.post("/uploaddepartmentfile", response_model=list[schemas.DepartmentIn])
async def upload_department_file(file: UploadFile, db: Session = Depends(get_db)):    
    try:
        return crud.process_department_data_from_file(file, db)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the CSV file")
    except csv.Error as csv_error:
        raise HTTPException(status_code=400, detail=f"CSV file error: {csv_error}")
    except ValueError as validation_error:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except crud.CustomValueError as value_error:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data}) 
    finally:
        db.close()
        
@app.post("/uploadmajorfile", response_model=list[schemas.MajorIn])
async def upload_major_file(file: UploadFile, db: Session = Depends(get_db)):    
    try:
        return crud.process_major_data_from_file(file, db)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the CSV file")
    except csv.Error as csv_error:
        raise HTTPException(status_code=400, detail=f"CSV file error: {csv_error}")
    except ValueError as validation_error:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except crud.CustomValueError as value_error:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data}) 
    finally:
        db.close()
        
@app.post("/uploaddegreefile", response_model=list[schemas.DegreeIn])
async def upload_degree_file(file: UploadFile, db: Session = Depends(get_db)):    
    try:
        return crud.process_degree_data_from_file(file, db)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the CSV file")
    except csv.Error as csv_error:
        raise HTTPException(status_code=400, detail=f"CSV file error: {csv_error}")
    except ValueError as validation_error:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except crud.CustomValueError as value_error:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data}) 
    finally:
        db.close()

@app.post("/uploadfacultyfile", response_model=list[schemas.FacultyIn])
async def upload_faculty_file(file: UploadFile, db: Session = Depends(get_db)):    
    try:
        return crud.process_faculty_data_from_file(file, db)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the CSV file")
    except csv.Error as csv_error:
        raise HTTPException(status_code=400, detail=f"CSV file error: {csv_error}")
    except ValueError as validation_error:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except crud.CustomValueError as value_error:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data}) 
    finally:
        db.close()
#--------------------------------------------------------------------------------------------------
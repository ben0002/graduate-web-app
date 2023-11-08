from fastapi import FastAPI, Depends, HTTPException, Request, Response, Cookie, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

#from cas import CASClient

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

@app.get("/students", response_model=list[schemas.Student])
async def students(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
    admit_type: AdmitType | None = None, residency: Residencies | None = None, 
    student_type: StudentTypes | None = None, prelim_exam_date: date | None = None, 
    prelim_exam_passed: bool | None = None, first_term: int | None = None, 
    status: StudentStatus | None = None, campus_id: int | None = None 
):
    filters = {
        "admit_type": admit_type,
        "residency": residency,
        "student_type": student_type,
        "prelim_exam_date": prelim_exam_date,
        "prelim_exam_passed": prelim_exam_passed,
        "first_term": first_term,
        "status": status,
        "campus_id": campus_id,
    }   
    
    students = crud.get_students(db=db ,filters=filters, skip=skip, limit=limit)
    return students


    
    
@app.post("/uploadfile")
async def upload_student_file(file: UploadFile, db: Session = Depends(get_db)):    
    try:
        return crud.process_csv_file(file, db)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the CSV file")
    except csv.Error as csv_error:
        raise HTTPException(status_code=400, detail=f"CSV file error: {csv_error}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    return {"message": "CSV data uploaded and processed successfully"}
from fastapi import FastAPI, Depends, HTTPException, Request, Response, Cookie, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from datetime import timedelta, datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from jose import JWTError, jwt

from cas import CASClient

from enums import *
from datetime import date

import crud, schemas, models
from database import SessionLocal, engine

import csv

#models.Base.metadata.drop_all(engine)
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

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


SERVICE_URL = "https://bktp-gradpro-api2.discovery.cs.vt.edu/"
SECRET_KEY = "03588c9b6f5508ff6ab7175ba9b38a4d1366581fdc6468e8323015db7d68dac0" # key used to sign JWT token
ALGORITHM = "HS256" # algorithm used to sign JWT Token
ACCESS_TOKEN_EXPIRE_MINUTES = 45

# Creating the CAS CLIENT
cas_client = CASClient(
    version=2,
    service_url=f"{SERVICE_URL}/login?",
    server_url="https://login.vt.edu/profile/cas/",
    # CHANGE: If you want VT CS CAS, to be used instead of VT CAS
    # change the server_url to https://login.cs.vt.edu/cas/
)

# Routes related to CAS
@app.get("/login")
def login(request: Request, response: Response, db:Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    if jwt: # return user info
        try:
            verify_jwt(jwt)
            return JSONResponse(content={"message": "Logged in!"}, media_type="application/json")
        except Exception as e:
            response.delete_cookie("access_token")
    
    cas_ticket = request.query_params.get("ticket")
    if not cas_ticket:
        cas_login_url = cas_client.get_login_url()
        return JSONResponse(content={"redirect_url": cas_login_url}, media_type="application/json")

    (user, _, _) = cas_client.verify_ticket(cas_ticket)
    if not user:
        raise HTTPException(status_code=403, detail="Failed to verify ticket!")
    
    access_token = role_based(pid=user, cas_ticket=cas_ticket, db=db)
    if not access_token:
        raise HTTPException(status_code=404, detail="Student or Faculty does not exist in the system.")
    
    web_app_url = "https://bktp-gradpro2.discovery.cs.vt.edu/"
    response = RedirectResponse(web_app_url)
    response.set_cookie(key="access_token", value=access_token, httponly=True, domain=".discovery.cs.vt.edu",
                        samesite="None", secure=True)
    
    return response

@app.get("/logout")
def logout(response: Response):
    cas_logout_url = cas_client.get_logout_url(SERVICE_URL)
    response.delete_cookie("access_token")
    return {"redirect_url": cas_logout_url}

#------------------- non-cas --------------------#

#------------------- JWT -----------------------#

def role_based(pid: str, cas_ticket, db: Session):
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    email = f"{pid}@vt.edu"
    faculty = crud.get_faculty(db=db, filters={"email":email},
                        skip=0, limit=1)
    if(len(faculty) != 0):
        data = {
            "sub": email,
            "faculty": True,
            "privilege": faculty[0].privilege_level,
            "id": faculty[0].id,
            "cas_ticket": cas_ticket
        }
        return create_access_token(data=data, expires_delta=access_token_expires)
    
    student = crud.get_students(db=db, filters={"email":email}, skip=0, limit=1)
    if(len(student) != 0):
        data = {
            "sub": email,
            "faculty": False,
            "id": student[0].id,
            "cas_ticket": cas_ticket
        }
        return create_access_token(data=data, expires_delta=access_token_expires)
    
    return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt(token: Annotated[str | None, Cookie()] = None):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"access_token": "jwt"},
        )
    
#------------------- helper functions -----------#
def pagination(skip: int, limit: int, response: list):
    total_responses = len(response)
    if skip < total_responses:
        response = response[skip:]
    else:
        return []
    
    if limit < total_responses:
        response = response[:limit]
    
    return response

#-------------------------------------- start of /students endpoints -------------------------------#

# ----------- lump info student page endpoints --------------------#
# 'student': {}, 'advisors': [], 'programs': [], 'campus': {}, 'POS_info': []}
@app.get("/students/login_info", response_model=schemas.studentCard)
def get_login_page_info(student_id: int | None = None, access_token:str = Cookie(...), db: Session=Depends(get_db)):
    
    payload = verify_jwt(access_token)
    if student_id is None:
        student_id = payload.get("id")
    student = crud.get_students(db=db, filters={"id": student_id}, skip=0, limit=1)[0]
    #student = crud.get_students(db=db, filters={"id": student_id}, skip=0, limit=1)[0]
    
    response = schemas.studentCard(
        info=student,
        campus=student.campus,
        advisors=[schemas.StudentAdvisorOut(
                    id=student_advisor.advisor.id,
                    first_name=student_advisor.advisor.first_name,
                    email=student_advisor.advisor.email,
                    last_name=student_advisor.advisor.last_name,
                    dept_code=student_advisor.advisor.dept_code,
                    privilege_level=student_advisor.advisor.privilege_level,
                    advisor_role=student_advisor.advisor_role   
                ) for student_advisor in student.advisors],
        programs=[schemas.ProgramEnrollmentOut(id=program.id, major=program.major, degree=program.degree, concentration=program.concentration,
                                               enrollment_date=program.enrollment_date) for program in student.programs],
        pos=student.pos
    )
    
    return response

@app.get("/students/progress_page_info", response_model=schemas.progressPage)
def get_progress_page(student_id: int | None = None, db: Session=Depends(get_db), access_token:str = Cookie(...)):
    
    payload = verify_jwt(access_token)
    if student_id is None:
        student_id = payload.get("id")
    
    tasks = student_progress(student_id=student_id, skip=0, limit=100, db=db, access_token=access_token)
    response = schemas.progressPage(
        milestones= [task for task in tasks if task.milestone],
        requirements= [task for task in tasks if task.requirement],
        funding=student_funding(student_id=student_id, skip=0, limit=100, db=db, access_token=access_token),
        employment=student_employments(student_id=student_id, skip=0, limit=100, db=db, access_token=access_token),
        to_do_list=student_events(student_id=student_id, skip=0, limit=0, db=db, access_token=access_token),
        courses=student_courses(student_id=student_id, skip=0, limit=100, db=db, access_token=access_token)
    )
    
    return response
    
    
    
    
@app.get("/students", response_model=list[schemas.StudentOut])
def students(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db), residency: Residencies | None = None, 
    student_status: StudentStatus | None = None, prelim_exam_date: date | None = None, 
    prelim_exam_passed: bool | None = None, first_term: int | None = None, 
    status: StudentStatus | None = None, campus_id: int | None = None, access_token:str = Cookie(...)
):
    verify_jwt(access_token)
    filters = {
        "va_residency": residency,
        "student_status": student_status,
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
def students_id(student_id: int, db: Session = Depends(get_db), access_token:str = Cookie(...)) -> schemas.StudentOut:
    
    verify_jwt(access_token)
    filter = {
        "id": student_id
    }
    
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    return student[0]

@app.get("/students/{student_id}/employments", response_model=list[schemas.EmploymentOut])
def student_employments(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db), access_token:str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    return pagination(skip=skip, limit=limit, response=student[0].employment)

@app.get("/students/{student_id}/funding", response_model=list[schemas.FundingOut])
def student_funding(student_id: int, skip: int | None = 0, limit: int | None = 100,  db: Session = Depends(get_db),
                    access_token: str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    return pagination(skip=skip, limit=limit, response=student[0].funding)

@app.get("/students/{student_id}/advisors", response_model=list[schemas.StudentAdvisorOut])
def student_advisors(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db), access_token: str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    advisors = []
    for student_advisor in student[0].advisors:
        advisors.append(
            schemas.StudentAdvisorOut(
                id=student_advisor.advisor.id,
                first_name=student_advisor.advisor.first_name,
                email=student_advisor.advisor.email,
                last_name=student_advisor.advisor.last_name,
                dept_code=student_advisor.advisor.dept_code,
                privilege_level=student_advisor.advisor.privilege_level,
                advisor_role=student_advisor.advisor_role   
            )
        )
        
    return pagination(skip=skip, limit=limit, response=advisors)
  
    
@app.get("/students/{student_id}/events", response_model=list[schemas.EventOut])
def student_events(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db), access_token:str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    return pagination(skip=skip, limit=limit, response=student[0].events)

@app.get("/students/{student_id}/labs", response_model=list[schemas.StudentLabsOut])
def student_labs(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db), access_token:str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    return pagination(skip=skip, limit=limit, response=student[0].labs)

@app.get("/students/{student_id}/programs", response_model=list[schemas.ProgramEnrollmentOut])
def student_programs(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db), access_token:str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    programs = []
    for program in student[0].programs:
        programs.append(
            schemas.ProgramEnrollmentOut(
                id=program.id,
                major=program.major,
                degree=program.degree,
                enrollment_date=program.enrollment_date
            )
        )
    return pagination(skip=skip, limit=limit, response=programs)

@app.get("/students/{student_id}/progress-tasks", response_model=list[schemas.ProgressOut])
def student_progress(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db), access_token:str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    tasks = []
    for task in student[0].progress_tasks:
        tasks.append(
            schemas.ProgressOut(
                id=task.id,
                ideal_completion_date=task.ideal_completion_date,
                requirement=task.requirement,
                milestone=task.milestone,
                deadline=task.deadline,
                completion_date=task.completion_date,
                approved=task.approved,
                note=task.note,
                exempt=task.exempt
            )
        )
    return pagination(skip=skip, limit=limit, response=tasks)

@app.get("/students/{student_id}/courses", response_model=list[schemas.CourseEnrollmentOut])
def student_courses(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db), access_token:str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    return pagination(skip=skip, limit=limit, response=student[0].courses)

@app.get("/students/{student_id}/pos", response_model=list[schemas.StudentPOSOut])
def student_pos(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db), access_token: str = Cookie(...)):
    
    verify_jwt(access_token)
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    return pagination(skip=skip, limit=limit, response=student[0].pos)

@app.get("/students/{student_id}/messages", response_model=list[schemas.MessageOut])
def student_messages(student_id: int, db: Session = Depends(get_db), skip: int | None = 0, limit: int | None = 100, access_token: str = Cookie(...)):
    
    payload = verify_jwt(access_token)
    
    filter = {"id": student_id}
    if(payload.get('faculty') == True):
        filter.update({"private", False})
        
    messages=crud.get_messages(db=db, filters=filter,skip=skip, limit=limit)
    return messages
    
    
@app.post("/students", status_code=201)
def create_students(students: list[schemas.CreateStudent], db:Session = Depends(get_db)):
    try:
        for student in students:
            
            student_data = {
                "first_name" :student.first_name,
                "middle_name": student.middle_name,
                "last_name":student.last_name,
                "citizenship":student.citizenship,
                "va_residency":student.va_residency,
                "status":student.status,
                "email":student.email,
                "phone_number": student.phone_number,
                "pronouns": student.pronouns,
                "gender":student.gender,
                "advisory_committee":student.advisory_committee,
                "prelim_exam_date":student.prelim_exam_date, # do we drop this column?
                "plan_submit_date":student.plan_submit_date,
                "prelim_exam_pass":student.prelim_exam_pass,
                "proposal_meeting":student.proposal_meeting,
                "progress_meeting":student.progress_meeting,
                "ETD_submitted":student.ETD_submitted,
                "final_exam":student.final_exam,
                "graduation_date":student.graduation_date,
                "enrollment_term":student.enrollment_term,
                "enrollment_year":student.enrollment_year
            }
            
            student_id = crud.insert_student(data=student_data, db=db)
            for program in student.program_enrollments:
                
                #major_id = crud.find_major(major_name=program.major, db=db, row_number=0)
                #degree_id = crud.find_degree(degree_name=program.degree, db=db, row_number=0)
                program_data = schemas.ProgramEnrollmentIn(
                    student_id=student_id,
                    degree_id=program.degree_id,
                    major_id=program.major_id,
                    enrollment_date=program.enrollment_date
                )
                crud.insert_program_enrollment(program=program_data, db=db)
            
            #advisor_name = f"{student.main_advisor.last_name},{student.main_advisor.first_name}"
            #advisor_id = crud.find_advisor(advisor_name=advisor_name, db=db, row_number=0)

            crud.insert_student_advisor_from_file(advisor_id=student.main_advisor_id, student_id=student_id, role=AdvisorRole.MAIN_ADVISOR, db=db)
            
            for co_advisor_id in student.co_advisors_ids:
                #advisor_name = f"{co_advisor.last_name},{co_advisor.first_name}"
                #advisor_id = crud.find_advisor(advisor_name=advisor_name, db=db, row_number=0)
                crud.insert_student_advisor_from_file(advisor_id=co_advisor_id, student_id=student_id, role=AdvisorRole.CO_ADVISOR, db=db)
            
        db.commit()    
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    
    
@app.post("/students/{student_id}/events", response_model=schemas.EventIn)
async def create_student_event(student_id: int, event: schemas.EventIn, access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        verify_jwt(access_token)
        #student_id = payload.get("id")
        event.student_id = student_id
        db_event = models.Event(**event.dict())
        db.add(db_event)
        db.commit()
        return db_event
    except IntegrityError as constraint_violation:
        db.rollback()
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.post("/students/{student_id}/employments", response_model=schemas.EmploymentOut)
async def create_student_employment(student_id: int, employment: schemas.EmploymentIn, access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        verify_jwt(access_token)
        #student_id = payload.get("id")
        #employment.student_id = student_id
        db_employment = models.Employment(**employment.dict(), student_id=student_id)
        db.add(db_employment)
        db.commit()
        return db_employment
        
    except IntegrityError as constraint_violation:
        db.rollback()
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
   
    
@app.post("/students/{student_id}/funding", response_model=schemas.FundingIn)
async def create_student_funding(student_id: int, funding: schemas.FundingIn, access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        verify_jwt(access_token)
        #student_id = payload.get("id")
        funding.student_id = student_id
        db_funding = models.Funding(**funding.dict())
        db.add(db_funding)
        db.commit()
        return db_funding
       
    except IntegrityError as constraint_violation:
        db.rollback()
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    
    
    
@app.post("/students/{student_id}/labs", response_model=schemas.StudentLabsOut)
async def create_student_lab(student_id: int, lab: schemas.StudentLabsIn, access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        verify_jwt(access_token)
       # lab.student_id = student_id
        db_lab = models.StudentLabs(**lab.dict(), student_id=student_id)
        db.add(db_lab)
        db.commit()
        return db_lab
    
    except IntegrityError as constraint_violation:
        
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
   
    

@app.post("/students/{student_id}/courses", response_model=schemas.CourseEnrollmentOut)
async def create_student_course(student_id: int, course: schemas.CourseEnrollmentIn, access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        verify_jwt(access_token)
        course.pos_id = crud.find_studentpos(student_id, db)
        db_course = models.CourseEnrollment(**course.dict(), student_id=student_id)
        db.add(db_course)
        db.commit()
        return db_course
    
    except IntegrityError as constraint_violation:
        db.rollback()
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.post("/students/{student_id}/pos", response_model=schemas.StudentPOSIn)
async def create_student_pos(student_id: int, pos: schemas.StudentPOSIn,access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        verify_jwt(access_token)
        pos.student_id = student_id
        db_pos = models.StudentPOS(**pos.dict())
        db.add(db_pos)
        db.commit()
        return db_pos
    
    except IntegrityError as constraint_violation:
        db.rollback()
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.post("/students/{student_id}/advisors/{advisor_id}", response_model=schemas.CreateStudentAdvisor)
async def create_student_advisor(student_id: int, advisor_id: int, role: schemas.StudentAdvisorIn, 
                                 access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        #payload = verify_jwt(access_token) this may need for privilege level
        db_advisor = models.StudentAdvisor(
            advisor_id = advisor_id,
            student_id = student_id,
            advisor_role = role.advisor_role
        )
        db.add(db_advisor)
        db.commit()
        return db_advisor
    
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), "problematic_row": value_error.row_data}) 
    except IntegrityError as constraint_violation:
        db.rollback()
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.post("/requirement", response_model=schemas.RequirementIn)
async def create_requirement(progress_requirement: schemas.RequirementIn, access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        ##payload = verify_jwt(access_token) this may need for privilege level
        return crud.insert_requirement(progress_requirement, db=db)
    
    except IntegrityError as constraint_violation:
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
        
@app.post("/milestone", response_model= schemas.MilestoneIn)
async def create_milestone(progress_milestone: schemas.MilestoneIn, access_token = Cookie(...), db:Session = Depends(get_db)):
    try:
        #payload = verify_jwt(access_token) this may need for privilege level
       
        return crud.insert_milestone(milestone=progress_milestone, db=db)
    
    except IntegrityError as constraint_violation:
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
        
@app.post("/students/{student_id}/progress", response_model= schemas.ProgressIn)
async def create_progress(progress: schemas.ProgressIn, db:Session = Depends(get_db)):
    try:
        #payload = verify_jwt(access_token) this may need for privilege level
        if crud.check_either_one(progress):
            progress_db = models.Progress(**progress.dict())
            db.add(progress_db)
            db.commit()
            db.refresh(progress_db)
            return progress_db
        else:
            raise {"Milestone, Requirement, and Custom milestone can be exisited either one"} 
    except IntegrityError as constraint_violation:
        HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
#------------------------------Student Delete Endpoint--------------------------    
@app.delete("/students/{student_id}", status_code=200)
async def delete_student(student_id : int, access_token = Cookie(...), db:Session = Depends(get_db)):
    #payload = verify_jwt(access_token) this may need for privilege level
    filter = {"id" : student_id}
    student = crud.delete_data(db=db, filter=filter, model=models.Student)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
@app.delete("/students/{student_id}/employments/{employment_id}", status_code=200)
async def delete_employment(student_id:int, employment_id: int, access_token = Cookie(...), db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : employment_id,
        "student_id" : student_id
        }
    student = crud.delete_data(db=db, filter=filter, model=models.Employment)
    if not student:
        raise HTTPException(status_code=404, detail=f"Employment with the given student id: {student_id} does not exist.")
    return {"Message": "Deletion Successful"}

    
@app.delete("/students/{student_id}/funding/{funding_id}", status_code=200)
async def delete_funding(student_id:int, funding_id : int, access_token = Cookie(...), db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : funding_id,
        "student_id" : student_id
        }
    student = crud.delete_data(db=db, filter=filter, model=models.Funding)
    if not student:
        raise HTTPException(status_code=404, detail=f"Funding with the given student id: {student_id} does not exist.")


@app.delete("/students/{student_id}/advisors/{advisor_id}", status_code=200)
async def delete_advisor(student_id : int, advisor_id : int, db:Session = Depends(get_db)):
    #payload = verify_jwt(access_token) this may need for privilege level
    
    filter = {
        "advisor_id" : advisor_id,
        "student_id" : student_id
        }
    student = crud.delete_data(db=db, filter=filter, model=models.StudentAdvisor)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student Advisor with the given student id: {student_id} does not exist.")
    
@app.delete("/students/{student_id}/events/{event_id}", status_code=200)
async def delete_event(student_id:int, event_id: int, access_token = Cookie(...), db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : event_id,
        "student_id" : student_id
        }
    student = crud.delete_data(db=db, filter=filter, model=models.Event)
    if not student:
        raise HTTPException(status_code=404, detail=f"Event with the given student id: {student_id} does not exist.")

@app.delete("/{student_id}/labs/{lab_id}", status_code=200)
async def delete_lab(student_id: int, lab_id: int, access_token = Cookie(...), db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : lab_id,
        "student_id" : student_id
        }
    student = crud.delete_data(db=db, filter=filter, model=models.StudentLabs)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student Lab with the given student id: {student_id} does not exist.")
    return {"Message": "Deletion Successful!"}
    
@app.delete("/students/{student_id}/progress/{progress_id}", status_code=200)
async def delete_progress(student_id:int, progress_id: int, access_token = Cookie(...),db:Session = Depends(get_db)):
    
    verify_jwt(access_token)
    filter = {
        "id" : progress_id,
        "student_id" : student_id
        }
    student = crud.delete_data(db=db, filter=filter, model=models.Progress)
    if not student:
        raise HTTPException(status_code=404, detail=f"Progress with the given student id: {student_id} does not exist.")
    
@app.delete("/students/{student_id}/courses/{course_id}", status_code=200)
async def delete_course(student_id: int, course_id: int, access_token = Cookie(...), db:Session = Depends(get_db)):
    
    verify_jwt(access_token)
    filter = {
        "id" : course_id,
        "student_id" : student_id
        }
    student = crud.delete_data(db=db, filter=filter, model=models.CourseEnrollment)
    if not student:
        raise HTTPException(status_code=404, detail=f"Course with the given student id: {student_id} does not exist.")
    return {"Message": "Successfully deleted!"}

@app.delete("/students/{student_id}/pos/{pos_id}", status_code=200)
async def delete_pos(student_id:int, pos_id: int, access_token = Cookie(...), db:Session = Depends(get_db)):
    
    verify_jwt(access_token)
    filter = {
        "id" : pos_id,
        "student_id" : student_id
        }
    
    pos = crud.delete_data(db=db, filter=filter, model=models.StudentPOS)
    if not pos:
        raise HTTPException(status_code=404, detail=f"Student POS with the given student id: {student_id} does not exist.")

@app.delete("/requirement/{requirement_id}")
def delete_requirement(requirement_id: int, access_token= Cookie(...), db:Session = Depends(get_db)):
    
    verify_jwt(access_token)
    try:
        crud.delete_requirement(db=db, requirement_id=requirement_id)
    except:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Requirement ID with the given id: {requirement_id} does not exist.")
    
@app.delete("/milestone/{milestone_id}")
def delete_milestone(milestone_id: int, access_token = Cookie(...), db:Session = Depends(get_db)):
    
    verify_jwt(access_token)
    try:
        crud.delete_milestone(db=db, milestone_id=milestone_id)
    except:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Milestone ID with the given id: {milestone_id} does not exist.")
     
@app.patch("/requirement/{requirement_id}", response_model=schemas.RequirementOut)
def update_requirement(update_fields: schemas.RequirementPatch, requirement_id: int, access_token = Cookie(...), 
                       db:Session = Depends(get_db)):
    
    verify_jwt(access_token)
    try:
        return crud.update_requirement(db=db, requirement_id=requirement_id, data=update_fields)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Requirement ID with the given id: {requirement_id} does not exist. Error: {e}")
    
@app.patch("/milestone/{milestone_id}", response_model=schemas.MilestoneOut)
def update_requirement(update_fields: schemas.MilestonePatch, milestone_id: int, access_token = Cookie(...), 
                       db:Session = Depends(get_db)):
    verify_jwt(access_token)
    try:
        return crud.update_milestone(db=db, milestone_id=milestone_id, data=update_fields)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Milestone ID with the given id: {milestone_id} does not exist. Error: {e}")

#---------------------------------------- end of /students endpoints --------------------------------------------#


@app.delete("/students/{student_id}/programs/{program_id}", status_code=200)
async def delete_programEnrollment(student_id : int, program_id: int, db:Session = Depends(get_db)):
    try:
        crud.delete_program_enrollment(db=db, program_id=program_id)
    except: 
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Program with the given student id: {student_id} does not exist.")

#--------------------------------- Patch Student EndPoint--------------------------
@app.patch("/student/{student_id}", response_model=schemas.StudentOut)
async def update_student(student_id : int, student_data:schemas.UpdateStudent, access_token = Cookie(...),db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : student_id
    }
    try:
        return crud.update_data(db, filter, models.Student, student_data)
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    
@app.patch("/student/{student_id}/employments/{employment_id}", response_model=schemas.EmploymentOut)
async def update_student_employment(student_id: int, employment_id: int, employment_data:schemas.UpdateEmployment, access_token = Cookie(...) ,db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : employment_id,
        "student_id":student_id
    }
    try:
        return crud.update_data(db, filter, models.Employment, employment_data)
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.patch("/student/{student_id}/fundings/{funding_id}", response_model=schemas.FundingOut)
async def update_student_funding(student_id: int, funding_id: int, funding_data:schemas.UpdateFunding, access_token = Cookie(...),db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : funding_id,
        "student_id": student_id
    }
    try:
        return crud.update_data(db, filter, models.Funding, funding_data)
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    
@app.patch("/student/{student_id}/events/{event_id}", response_model=schemas.EventOut)
async def update_student_funding(student_id: int, event_id: int, event_data:schemas.UpdateEvent, access_token = Cookie(...),db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : event_id,
        "student_id": student_id
    }
    try:
        return crud.update_data(db, filter, models.Event, event_data)
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.patch("/student/{student_id}/advisors/{advisor_id}", response_model=schemas.ResponseUpdateStudentAdvisor)
async def update_student_advisor(student_id: int, advisor_id: int, advisor_data:schemas.UpdateStudentAdvisor, access_token = Cookie(...) ,db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "advisor_id" : advisor_id,
        "student_id" : student_id
    }
    try:
        return crud.update_data(db, filter, models.StudentAdvisor, advisor_data)
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.patch("/student/{student_id}/labs/{lab_id}", response_model=schemas.StudentLabsOut)
async def update_student_lab(student_id: int, lab_id: int, lab_data:schemas.UpdateStudentLabs, access_token = Cookie(...),db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : lab_id,
        "student_id": student_id
    }
    try:
        return crud.update_data(db, filter, models.StudentLabs, lab_data)
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    
@app.patch("/student/{student_id}/courses/{course_id}", response_model=schemas.CourseEnrollmentOut)
async def update_student_course(student_id: int, course_id: int, course_data:schemas.UpdateCourseEnrollment, access_token = Cookie(...),db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : course_id,
        "student_id": student_id
    }
    try:
        return crud.update_data(db, filter, models.CourseEnrollment, course_data)
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.patch("/student/{student_id}/pos/{pos_id}", response_model=schemas.StudentPOSOut)
async def update_student_pos(student_id: int, pos_id: int, pos_data:schemas.UpdateStudentPOS, access_token = Cookie(...),db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : pos_id,
        "student_id": student_id
    }
    try:
        return crud.update_data(db, filter, models.StudentPOS, pos_data)
    except crud.CustomValueError as value_error:
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")


@app.patch("/student/{student_id}/program/{programenrollment_id}", response_model=schemas.ResponseUpdateProgramEnrollment)
async def update_student_programenrollment(student_id: int, programenrollment_id: int, programenrollment_data:schemas.UpdateProgramEnrollment, 
                                            access_token = Cookie(...),db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : programenrollment_id,
        "student_id": student_id
    }
    try:
        return crud.update_programenrollment_data(db, filter, models.ProgramEnrollment, programenrollment_data)
    except crud.CustomValueError as value_error:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")

@app.patch("/student/{student_id}/progress/{progress_id}", response_model=schemas.ResponsedUpdateProgress)
async def update_student_programenrollmen(student_id: int, progress_id: int, progress_data:schemas.UpdateProgress, access_token = Cookie(...), db:Session = Depends(get_db)):
    verify_jwt(access_token)
    filter = {
        "id" : progress_id,
        "student_id": student_id
    }
    try:
        return crud.update_progress_data(db, filter, models.Progress, progress_data)
    except crud.CustomValueError as value_error:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error_message": str(value_error), 
                                                     "problematic_row": value_error.row_data})
    except ValueError as validation_error:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Validation error: {str(validation_error)}")
    
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    
#---------------------------------------- end of /students endpoints --------------------------------------------#
    
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

#do we also need professor and amdit for it?
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
async def degrees(db: Session = Depends(get_db), skip: int | None = 0, limit: int | None = 100):
    
    return crud.get_degrees(db, None, skip, limit)

@app.get("/degrees/{degree_id}", response_model=schemas.DegreeOut)
async def degree(degree_id: int, db: Session = Depends(get_db)):
    
    filter = { "id": degree_id}
    
    degree = crud.get_degrees(db, filter, 0, 1)
    
    if(len(degree) == 0):
        raise HTTPException(status_code=404, detail=f"Degree with the given id: {degree_id} does not exist.")
    return degree[0]

@app.get("/majors", response_model=list[schemas.MajorOut])
async def majors(db: Session = Depends(get_db), skip: int | None = 0, limit: int | None = 100):
    
    return crud.get_majors(db, None, skip, limit)

@app.get("/majors/{major_id}", response_model=schemas.MajorOut)
async def major(major_id: int, db: Session = Depends(get_db), skip: int | None = 0, limit: int | None = 100):
    
    filters = {'id': major_id}
    
    major = crud.get_majors(db, filters, skip, limit)
    if(len(major) == 0):
        raise HTTPException(status_code=404, detail=f"Major with the given id: {major_id} does not exist.")
    return major[0]

@app.get("/campus", response_model=list[schemas.CampusOut])
async def campuses(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db), campus_name: str | None = None): 
    filters = {
        "name": campus_name
    }
    campus = crud.get_campus(db, filters, skip, limit)
    return campus

@app.get("/campus/{campus_id}", response_model=schemas.CampusOut)
async def campus(campus_id: int, db: Session = Depends(get_db)):
    filter = { "id": campus_id}
    campus = crud.get_campus(db, filter, 0, 1)
    if(len(campus) == 0):
        raise HTTPException(status_code=404, detail=f"Campus with the given id: {campus_id} does not exist.")
    return campus[0]

@app.get("/departments", response_model=list[schemas.DepartmentOut])
async def departments(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db), department_name: str | None = None):
    filter = {
        "name": department_name
    }
    department = crud.get_department(db, filter, skip, limit)
    return department

@app.get("/departments/{dept_code}", response_model=schemas.DepartmentOut)
async def department(dept_code: int, db: Session = Depends(get_db)):
    filter = { "dept_code": dept_code}
    department = crud.get_department(db, filter, 0, 1)
    if(len(department) == 0):
        raise HTTPException(status_code=404, detail=f"Department with the given id: {dept_code} does not exist.")
    return department[0]

@app.get("/programEnrollments", response_model=list[schemas.ProgramEnrollmentOut])
async def programEnrollments(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    programEnrollment = crud.get_programEnrollment(db, None, skip, limit)
    return programEnrollment

@app.get("/programEnrollments/{programEnrollment_id}", response_model=schemas.ProgramEnrollmentOut)
async def programEnrollment(programEnrollment_id: int, db: Session = Depends(get_db)):
    filter = { "id": programEnrollment_id}
    programEnrollment = crud.get_programEnrollment(db, filter, 0, 1)
    if(len(programEnrollment) == 0):
        raise HTTPException(status_code=404, detail=f"Program Enrollment with the given id: {programEnrollment_id} does not exist.")
    return programEnrollment[0]


@app.get("/studentLabs/{studentLab_id}", response_model=schemas.StudentLabsOut)
async def studentLab(studentLab_id: int, db: Session = Depends(get_db)):
    filter = { "id": studentLab_id}
    studentLab = crud.get_studentLab(db, filter, 0, 1)
    if(len(studentLab) == 0):
        raise HTTPException(status_code=404, detail=f"Student Lab with the given id: {studentLab_id} does not exist.")
    return studentLab[0]

@app.get("/employments", response_model=list[schemas.EmploymentOut])
async def employments(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    employments = crud.get_employment(db, None, skip, limit)
    return employments

@app.get("/employments/{employment_id}", response_model=schemas.EmploymentOut)
async def employment(employment_id: int, db: Session = Depends(get_db)):
    filter = { "id": employment_id}
    employment = crud.get_employment(db, filter, 0, 1)
    if(len(employment) == 0):
        raise HTTPException(status_code=404, detail=f"Employment with the given id: {employment_id} does not exist.")
    return employment[0]

@app.get("/funding", response_model=list[schemas.FundingOut])
async def fundings(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    fundings = crud.get_funding(db, None, skip, limit)
    return fundings

@app.get("/funding/{funding_id}", response_model=schemas.FundingOut)
async def funding(funding_id: int, db: Session = Depends(get_db)):
    filter = { "id": funding_id}
    funding = crud.get_funding(db, filter, 0, 1)
    if(len(funding) == 0):
        raise HTTPException(status_code=404, detail=f"Funding with the given id: {funding_id} does not exist.")
    return funding[0]

@app.get("/events", response_model=list[schemas.EventOut])
async def events(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    events = crud.get_event(db, None, skip, limit)
    return events

@app.get("/events/{event_id}", response_model=schemas.EventOut)
async def event(event_id: int, db: Session = Depends(get_db)):
    filter = { "id": event_id}
    event = crud.get_event(db, filter, 0, 1)
    if(len(event) == 0):
        raise HTTPException(status_code=404, detail=f"Event with the given id: {event_id} does not exist.")
    return event[0]

@app.get("/requirements", response_model=list[schemas.RequirementOut])
async def requirements(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db), requirement_name: str | None = None, major_id: int | None = None, degree_id: int | None = None):
    filter = { "name": requirement_name,
               "major_id" : major_id,
               "degree_id" : degree_id
            }
    requirements = crud.get_requirement(db, filter, skip, limit)
    return requirements

@app.get("/requirements/{requirement_id}", response_model=schemas.RequirementOut)
async def requirement(requirement_id: int, db: Session = Depends(get_db)):
    filter = { "id": requirement_id}
    requirement = crud.get_requirement(db, filter, 0, 1)
    if(len(requirement) == 0):
        raise HTTPException(status_code=404, detail=f"Requirement with the given id: {requirement_id} does not exist.")
    return requirement[0]

@app.get("/milestones", response_model=list[schemas.MilestoneOut])
async def milestones(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    milestones = crud.get_milestone(db, None, skip, limit)
    return milestones

@app.get("/milestones/{milestone_id}", response_model=schemas.MilestoneOut)
async def milestone(milestone_id: int, db: Session = Depends(get_db)):
    filter = { "id": milestone_id}
    milestone = crud.get_milestone(db, filter, 0, 1)
    if(len(milestone) == 0):
        raise HTTPException(status_code=404, detail=f"Milestone with the given id: {milestone_id} does not exist.")
    return milestone[0]

@app.get("/progress", response_model=list[schemas.ProgressOut])
async def progresses(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    progresses = crud.get_progress(db, None, skip, limit)
    return progresses

@app.get("/progress/{progress_id}", response_model=schemas.ProgressOut)
async def progress(progress_id: int, db: Session = Depends(get_db)):
    filter = { "id": progress_id}
    progress = crud.get_progress(db, filter, 0, 1)
    if(len(progress) == 0):
        raise HTTPException(status_code=404, detail=f"Progress with the given id: {progress_id} does not exist.")
    return progress[0]

@app.get("/courseEnrollments", response_model=list[schemas.CourseEnrollmentOut])
async def courseEnrollments(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    courseEnrollments = crud.get_courseEnrollment(db, None, skip, limit)
    return courseEnrollments

@app.get("/courseEnrollments/{courseEnrollment_id}", response_model=schemas.CourseEnrollmentOut)
async def courseEnrollment(courseEnrollment_id: int, db: Session = Depends(get_db)):
    filter = { "id": courseEnrollment_id}
    courseEnrollment = crud.get_courseEnrollment(db, filter, 0, 1)
    if(len(courseEnrollment) == 0):
        raise HTTPException(status_code=404, detail=f"CourseEnrollment with the given id: {courseEnrollment_id} does not exist.")
    return courseEnrollment[0]

@app.get("/pos", response_model=list[schemas.StudentPOSOut])
async def studentPOSs(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    studentPOS = crud.get_studentPOS(db, None, skip, limit)
    return studentPOS

@app.get("/studentPOS/{studentPOS_id}", response_model=schemas.StudentPOSOut)
async def studentPOS(studentPOS_id: int, db: Session = Depends(get_db)):
    filter = { "id": studentPOS_id}
    studentPOS = crud.get_studentPOS(db, filter, 0, 1)
    if(len(studentPOS) == 0):
        raise HTTPException(status_code=404, detail=f"StudentPOS with the given id: {studentPOS_id} does not exist.")
    return studentPOS[0]

#---------------------------------File Upload EndPoints----------------------------------------
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
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
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
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
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
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
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
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
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
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
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
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    finally:
        db.close()
    
@app.post("/uploadmilestonefile", response_model=list[schemas.MilestoneIn])
async def upload_milestone_file(file: UploadFile, db: Session = Depends(get_db)):    
    try:
        return crud.process_milestone_data_from_file(file, db)
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
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    finally:
        db.close()

@app.post("/uploadrequirementfile", response_model=list[schemas.RequirementIn])
async def upload_requirement_file(file: UploadFile, db: Session = Depends(get_db)):  
    try:
        return crud.process_requirement_data_from_file(file, db)
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
    except IntegrityError as constraint_violation:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Integrity error: {str(constraint_violation)}")
    finally:
        db.close()
#--------------------------------------------------------------------------------------------------
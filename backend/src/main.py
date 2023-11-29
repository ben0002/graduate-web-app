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

@app.get("/api/")
def read_root():
    return {"message": "Hello, World!"}


SERVICE_URL = "https://bktp-gradpro-api2.discovery.cs.vt.edu/"
SECRET_KEY = "03588c9b6f5508ff6ab7175ba9b38a4d1366581fdc6468e8323015db7d68dac0" # key used to sign JWT token
ALGORITHM = "HS256" # algorithm used to sign JWT Token
ACCESS_TOKEN_EXPIRE_MINUTES = 120

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
def login(request: Request, response: Response, db: Session = Depends(get_db)):

    delete_token = False
    delete_token = False
    jwt = request.cookies.get("access_token")
    if jwt: # return user info
        response = getUserData(jwt, db)
        if(response):
            return response
        else:
            delete_token = True
            delete_token = True

    cas_ticket = request.query_params.get("ticket")
    if not cas_ticket:
        cas_login_url = cas_client.get_login_url()
        response = JSONResponse(content={"redirect_url": cas_login_url}, media_type="application/json")
        if(delete_token):
            response.delete_cookie("access_token")
        return response
        response = JSONResponse(content={"redirect_url": cas_login_url}, media_type="application/json")
        if(delete_token):
            response.delete_cookie("access_token")
        return response

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
    except JWTError as e:
        return None
    

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

def getUserData(jwt: str, db: Session):
    token = verify_jwt(jwt)
    if(not token):
        return token
    
    isFaculty = token.get("faculty")
    if(isFaculty):
        "retrieve faculty info and list of students or other permission based information"
        return JSONResponse(content={'faculty': {}}, media_type='application/json')

    userData = {'student': {}, 'advisors': [], 'programs': [], 'campus': {}, 'POS_info': []}

    students = crud.get_students(db=db, filters={"id": token.get("id")})
    if len(students) == 0:
        raise HTTPException(status_code=404, detail=f"Student with valid access token does not exist.")
    student = students[0]

    # Fetch student information
    userData['student'] = student.as_dict()

    # Fetch advisors
    if student.advisors:
        userData['advisors'] = [{'name': advisor.advisor.first_name + ' ' + advisor.advisor.last_name, 'role': advisor.advisor_role} for advisor in student.advisors]

    # Fetch program enrollments
    if student.programs:
        for program_enrollment in student.programs:
            program_data = {
                "enrollment_date": program_enrollment.enrollment_date,
                "major": program_enrollment.major.name,
                "department": program_enrollment.major.dept_code,
                "degree": program_enrollment.degree.name
            }
            userData['programs'].append(program_data)

    # Fetch campus information
    if student.campus:
        userData['campus'] = {
            "name": student.campus.name,
            "address": student.campus.address
        }

    #if student.student_pos:
    #    userData['POS_info'] = {
    #        "approved": student.student_pos.approved,
    #        "approved_date": student.student_pos.approved_date,
    #        "chair": student.student_pos.chair,
    #        "co_chair": student.student_pos.co_chair
    #    }

    userData.update({'programs': []})
    programEnrollments = crud.get_programEnrollment(db=db, filters={"student_id": student_id})
    for program in programEnrollments:
        program_dict = program.as_dict()

        major_id = program_dict.get("major_id")
        majors = crud.get_majors(db=db, filters={"id": major_id})
        if(len(majors) == 0):
            raise HTTPException(status_code=404, detail=f"major with valid access token does not exist.")
        major_info = majors[0].as_dict()

        degree_id = program_dict.get("degree_id")
        degrees = crud.get_degrees(db=db, filters={"id": degree_id})
        if(len(degrees) == 0):
            raise HTTPException(status_code=404, detail=f"degree with valid access token does not exist.")
        degree_info = degrees[0].as_dict()

        userData.get("programs").append({"enrollment_date": program_dict.get("enrollment_date"), "major": major_info.get("name"), "department": major_info.get("dept_code"), "degree": degree_info.get("name")})
        
    campus_id = userData.get("campus_id")
    campuses = crud.get_campus(db=db, filters={"id": campus_id})
    if(len(campuses) == 0):
        raise HTTPException(status_code=404, detail=f"campus with valid access token does not exist.")
    campus_info = campuses[0].as_dict()

    userData.update({"campus_info": {"campus": campus_info.get("name"), "campus_addr": campus_info.get("address")}})

    userData.update({"POS_info": {}})
    #POS = crud.get_studentPOS(db=db, filters={"student_id": student_id})
    #if(len(POS) == 0):
    #    raise HTTPException(status_code=404, detail=f"POS with valid access token does not exist.")
    #POS_info = POS[0].as_dict()

    #userData.update({"POS_info": {"approved": POS_info.get("approved"), "approved_date": POS_info.get("approved_date"), "chair": POS_info.get("chair"), "co_chair": POS_info.get("co_chair"), "submitted": POS_info.get("submitted")}})

    userData.update({"courses": []})
    courses = crud.get_courseEnrollment(db=db, filters={"student_id": student_id})
    for course in courses:
        course_info = course.as_dict()
        course_info.pop("id")
        course_info.pop("student_id")
        course_info.pop("pos_id")
        userData.get("courses").append(course_info)

    return JSONResponse(content=userData, media_type='application/json')

@app.get("/student/progress")
async def student_progress(request: Request, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if not payload: 
        return HTTPException(status_code=401, detail="Access token has expired, please log in again")
    
    progressData = {"events": [], "milestones": [], "requirements": [], "funding": [], "employment": [], "courses": []}

    students = crud.get_students(db=db, filters={"id": payload.get("id")})
    if len(students) == 0:
        raise HTTPException(status_code=404, detail=f"Student with valid access token does not exist.")
    student = students[0]

    # Fetch events
    progressData['events'] = [event.as_dict() for event in student.events]

    # Fetch milestones
    for progress in student.progress_tasks:
        progress_info = progress.as_dict()
        progress_info.pop("student_id")
        if progress.milestone:
            milestone_info = progress.milestone.as_dict()
            progress_info.update({"name": milestone_info.get("name"), "desc": milestone_info.get("description")})
            progressData['milestones'].append(progress_info)
        else:
            requirement_info = progress.requirement.as_dict()
            progress_info.update({"name": requirement_info.get("name"), "desc": requirement_info.get("description")})
            progressData['requirements'].append(progress_info)

    # Fetch funding
    if student.funding:
        progressData['funding'] = [funding.as_dict() for funding in student.funding]

    # Fetch employment
    if student.employment:
        progressData['employment'] = [employment.as_dict() for employment in student.employment]

    return JSONResponse(content=progressData, media_type='application/json')

@app.get("/student/profile")
async def student_profile(request: Request, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")

    profileData = {"labs": [], 'messages': []}

    students = crud.get_students(db=db, filters={"id": payload.get("id")})
    if len(students) == 0:
        raise HTTPException(status_code=404, detail=f"Student with valid access token does not exist.")
    student = students[0]

    # Fetch student's labs
    if student.labs:
        profileData['labs'] = [lab.as_dict() for lab in student.labs]

    return JSONResponse(content=profileData, media_type='application/json')

@app.post("/student/event")
async def create_event(request: Request, event_data: schemas.EventIn, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")

    db_event = models.Event(**event_data.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.put("/student/event/{event_id}")
async def update_event(request: Request, event_id: int, db: Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    event_data = await request.json()  # Get the request body as JSON

    # Retrieve the event from the database using event_id
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.student_id == student_id).first()

    if not event:
        return {"message": "Event not found"}

    # Update the event attributes dynamically
    for field, value in event_data.items():
        setattr(event, field, value)

    db.add(event)
    db.commit()
    db.refresh(event)

    return event  # Return the updated event

@app.delete("/student/event/{event_id}")
async def delete_event(request: Request, event_id: int, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    db_event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.student_id == student_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}

@app.post("/students/milestone")
async def create_milestone(request: Request, milestone_data: schemas.MilestoneIn, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    isFaculty = payload['faculty']

    if isFaculty:
        if payload['privilege'] < 3:
            return HTTPException(status_code=401, detail="you do not have permission to perform this action")
    else:
        return HTTPException(status_code=401, detail="you do not have permission to perform this action")

    #populate progress table too
    db_milestone = models.Milestone(**milestone_data.dict())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@app.put("/students/milestone/{milestone_id}")
async def update_milestone(request: Request, milestone_id: int, db: Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    isFaculty = payload['faculty']

    if isFaculty:
        if payload['privilege'] < 3:
            return HTTPException(status_code=401, detail="you do not have permission to perform this action")
    else:
        return HTTPException(status_code=401, detail="you do not have permission to perform this action")

    # Retrieve the event from the database using event_id
    milestone = db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()
    if not milestone:
        return {"message": "Milestone not found"}

    milestone_data = await request.json()  # Get the request body as JSON
    # Update the event attributes dynamically
    for field, value in milestone_data.items():
        setattr(milestone, field, value)

    db.add(milestone)
    db.commit()
    db.refresh(milestone)

    return milestone  # Return the updated event

@app.delete("/students/milestone/{milestone_id}")
async def delete_milestone(request: Request, milestone_id: int, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    isFaculty = payload['faculty']

    if isFaculty:
        if payload['privilege'] < 3:
            return HTTPException(status_code=401, detail="you do not have permission to perform this action")
    else:
        return HTTPException(status_code=401, detail="you do not have permission to perform this action")

    db_milestone = db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()
    if db_milestone is None:
        raise HTTPException(status_code=404, detail="Milestone not found")
    db.delete(db_milestone)
    db.commit()
    return {"message": "Milestone deleted successfully"}

@app.post("/students/requirement")
async def create_requirement(request: Request, requirement_data: schemas.RequirementIn, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    isFaculty = payload['faculty']

    if isFaculty:
        if payload['privilege'] < 3:
            return HTTPException(status_code=401, detail="you do not have permission to perform this action")
    else:
        return HTTPException(status_code=401, detail="you do not have permission to perform this action")

    #populate progress table too
    db_requirement = models.Requirement(**requirement_data.dict())
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

@app.put("/students/requirement/{requirement_id}")
async def update_requirement(request: Request, requirement_id: int, db: Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    isFaculty = payload['faculty']

    if isFaculty:
        if payload['privilege'] < 3:
            return HTTPException(status_code=401, detail="you do not have permission to perform this action")
    else:
        return HTTPException(status_code=401, detail="you do not have permission to perform this action")

    # Retrieve the event from the database using event_id
    requirement = db.query(models.Requirement).filter(models.Requirement.id == requirement_id).first()
    if not requirement:
        return {"message": "Requirement not found"}

    requirement_data = await request.json()  # Get the request body as JSON
    # Update the event attributes dynamically
    for field, value in requirement_data.items():
        setattr(requirement, field, value)

    db.add(requirement)
    db.commit()
    db.refresh(requirement)

    return requirement  # Return the updated event

@app.delete("/students/requirement/{requirement_id}")
async def delete_requirement(request: Request, requirement_id: int, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    isFaculty = payload['faculty']

    if isFaculty:
        if payload['privilege'] < 3:
            return HTTPException(status_code=401, detail="you do not have permission to perform this action")
    else:
        return HTTPException(status_code=401, detail="you do not have permission to perform this action")

    db_requirement = db.query(models.Requirement).filter(models.Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    db.delete(db_requirement)
    db.commit()
    return {"message": "Requirement deleted successfully"}

@app.post("/student/funding")
async def create_funding(request: Request, funding_data: schemas.FundingIn, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")

    db_funding = models.Funding(**funding_data.dict())
    db.add(db_funding)
    db.commit()
    db.refresh(db_funding)
    return db_funding

@app.put("/student/funding/{funding_id}")
async def update_funding(request: Request, funding_id: int, db: Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    # Retrieve the event from the database using event_id
    funding = db.query(models.Funding).filter(models.Funding.id == funding_id, models.Funding.student_id == student_id).first()
    if not funding:
        return {"message": "Funding not found"}

    funding_data = await request.json()
    # Update the event attributes dynamically
    for field, value in funding_data.items():
        setattr(funding, field, value)

    db.add(funding)
    db.commit()
    db.refresh(funding)

    return funding  # Return the updated event

@app.delete("/student/funding/{funding_id}")
async def delete_funding(request: Request, funding_id: int, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    db_funding = db.query(models.Funding).filter(models.Funding.id == funding_id, models.Funding.student_id == student_id).first()
    if db_funding is None:
        raise HTTPException(status_code=404, detail="Funding not found")
    db.delete(db_funding)
    db.commit()
    return {"message": "Funding deleted successfully"}

@app.post("/student/employment")
async def create_employment(request: Request, employment_data: schemas.EmploymentIn, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")

    db_employment = models.Employment(**employment_data.dict())
    db.add(db_employment)
    db.commit()
    db.refresh(db_employment)
    return db_employment

@app.put("/student/employment/{employment_id}")
async def update_employment(request: Request, employment_id: int, db: Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    # Retrieve the event from the database using event_id
    employment = db.query(models.Employment).filter(models.Employment.id == employment_id, models.Employment.student_id == student_id).first()
    if not employment:
        return {"message": "Employment not found"}

    employment_data = await request.json()
    # Update the event attributes dynamically
    for field, value in employment_data.items():
        setattr(employment, field, value)

    db.add(employment)
    db.commit()
    db.refresh(employment)

    return employment  # Return the updated event

@app.delete("/student/employment/{employment_id}")
async def delete_employment(request: Request, employment_id: int, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    db_employment = db.query(models.Employment).filter(models.Employment.id == employment_id, models.Employment.student_id == student_id).first()
    if db_employment is None:
        raise HTTPException(status_code=404, detail="Employment not found")
    db.delete(db_employment)
    db.commit()
    return {"message": "Employment deleted successfully"}

##TODO: check courses after POS
@app.post("/student/course")
async def create_course(request: Request, course_data: schemas.CourseEnrollmentIn, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")

    db_course = models.CourseEnrollment(**course_data.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.put("/student/course/{course_id}")
async def update_course(request: Request, course_id: int, db: Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    # Retrieve the event from the database using event_id
    course = db.query(models.CourseEnrollment).filter(models.CourseEnrollment.id == course_id, models.CourseEnrollment.student_id == student_id).first()
    if not course:
        return {"message": "Course not found"}

    course_data = await request.json()
    # Update the event attributes dynamically
    for field, value in course_data.items():
        setattr(course, field, value)

    db.add(course)
    db.commit()
    db.refresh(course)

    return course  # Return the updated event

@app.delete("/student/course/{course_id}")
async def delete_course(request: Request, course_id: int, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    db_course = db.query(models.CourseEnrollment).filter(models.CourseEnrollment.id == course_id, models.CourseEnrollment.student_id == student_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted successfully"}

@app.post("/student/lab")
async def create_lab(request: Request, lab_data: schemas.StudentLabsIn, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")

    db_lab = models.StudentLabs(**lab_data.dict())
    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)
    return db_lab

@app.put("/student/lab/{lab_id}")
async def update_lab(request: Request, lab_id: int, db: Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    # Retrieve the event from the database using event_id
    lab = db.query(models.StudentLabs).filter(models.StudentLabs.id == lab_id, models.StudentLabs.student_id == student_id).first()
    if not lab:
        return {"message": "Lab not found"}

    lab_data = await request.json()
    # Update the event attributes dynamically
    for field, value in lab_data.items():
        setattr(lab, field, value)

    db.add(lab)
    db.commit()
    db.refresh(lab)

    return lab  # Return the updated event

@app.delete("/student/lab/{lab_id}")
async def delete_lab(request: Request, lab_id: int, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    db_lab = db.query(models.StudentLabs).filter(models.StudentLabs.id == lab_id, models.StudentLabs.student_id == student_id).first()
    if db_lab is None:
        raise HTTPException(status_code=404, detail="Lab not found")
    db.delete(db_lab)
    db.commit()
    return {"message": "Lab deleted successfully"}

"""
@app.post("/student/pos")
async def create_pos(request: Request, pos_data: schemas.StudentPOSIn, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")

    db_pos = models.StudentPOS(**pos_data.dict())
    db.add(db_pos)
    db.commit()
    db.refresh(db_pos)
    return db_pos
"""

@app.put("/student/pos/{pos_id}")
async def update_pos(request: Request, pos_id: int, db: Session = Depends(get_db)):

    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    # Retrieve the event from the database using event_id
    pos = db.query(models.StudentPOS).filter(models.StudentPOS.id == pos_id, models.StudentPOS.student_id == student_id).first()
    if not pos:
        return {"message": "POS not found"}

    pos_data = await request.json()
    # Update the event attributes dynamically
    for field, value in pos_data.items():
        setattr(pos, field, value)

    db.add(pos)
    db.commit()
    db.refresh(pos)

    return pos  # Return the updated event

"""
@app.delete("/student/pos/{pos_id}")
async def delete_lab(request: Request, pos_id: int, db: Session = Depends(get_db)):
    jwt = request.cookies.get("access_token")
    payload = verify_jwt(jwt)
    if(not payload): 
        return HTTPException(status_code=401, detail="access token has expired, please log in again")
    student_id = payload['id']

    db_pos = db.query(models.StudentPOS).filter(models.StudentPOS.id == pos_id, models.StudentPOS.student_id == student_id).first()
    if db_pos is None:
        raise HTTPException(status_code=404, detail="POS not found")
    db.delete(db_pos)
    db.commit()
    return {"message": "POS deleted successfully"}
"""

#TODO: messages

#-------------------------------------- start of /students endpoints -------------------------------#
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

@app.get("/students/{student_id}/employments", response_model=list[schemas.EmploymentOut])
def student_employments(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db)):
    
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    return pagination(skip=skip, limit=limit, response=student[0].employment)

@app.get("/students/{student_id}/funding", response_model=list[schemas.FundingOut])
def student_funding(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db)):
    
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    return pagination(skip=skip, limit=limit, response=student[0].funding)

@app.get("/students/{student_id}/advisors", response_model=list[schemas.StudentAdvisorOut])
def student_advisors(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db)):
    
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
                middle_name=student_advisor.advisor.middle_name,
                last_name=student_advisor.advisor.last_name,
                dept_code=student_advisor.advisor.dept_code,
                privilege_level=student_advisor.advisor.privilege_level,
                advisor_role=student_advisor.advisor_role,
                email=student_advisor.advisor.email   
            )
        )
        
    return pagination(skip=skip, limit=limit, response=advisors)
  
@app.get("/students/{student_id}/events", response_model=list[schemas.EventOut])
def student_events(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db)):
    
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    return pagination(skip=skip, limit=limit, response=student[0].events)

@app.get("/students/{student_id}/labs", response_model=list[schemas.StudentLabsOut])
def student_labs(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db)):
    
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    
    return pagination(skip=skip, limit=limit, response=student[0].labs)

@app.get("/students/{student_id}/programs", response_model=list[schemas.ProgramEnrollmentOut])
def student_programs(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db)):
    
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
                        db: Session = Depends(get_db)):
    
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
                        db: Session = Depends(get_db)):
    
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    return pagination(skip=skip, limit=limit, response=student[0].courses)

@app.get("/students/{student_id}/pos", response_model=list[schemas.StudentPOSOut])
def student_pos(student_id: int, skip: int | None = 0, limit: int | None = 100, 
                        db: Session = Depends(get_db)):
    
    filter = {"id": student_id}
    student = crud.get_students(db=db, filters=filter)
    if(len(student) == 0):
        raise HTTPException(status_code=404, detail=f"Student with the given id: {student_id} does not exist.")
    return pagination(skip=skip, limit=limit, response=student[0].pos)

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

@app.get("/stages", response_model=list[schemas.StageOut])
async def stages(skip: int | None = 0, limit: int | None = 100, db: Session = Depends(get_db), stage_name: str | None = None, major_id: int | None = None, degree_id : int | None = None):
    filter = {
        "name" : stage_name,
        "major_id" : major_id,
        "degree_id" : degree_id
    }
    stages = crud.get_stage(db, None, skip, limit)
    return stages

@app.get("/stages/{stage_id}", response_model=schemas.StageOut)
async def stage(stage_id: int, db: Session = Depends(get_db)):
    filter = { "id": stage_id}
    stage = crud.get_stage(db, filter, 0, 1)
    if(len(stage) == 0):
        raise HTTPException(status_code=404, detail=f"Stage with the given id: {stage_id} does not exist.")
    return stage[0]

@app.get("/studentPOS", response_model=list[schemas.StudentPOSOut])
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

@app.post("/students", status_code=201)
async def create_students(students: list[schemas.StudentIn], db:Session = Depends(get_db)):
    for student in students:
        db_student = models.Student(**student.dict())
        db.add(db_student)
    db.commit()

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
#--------------------------------------------------------------------------------------------------
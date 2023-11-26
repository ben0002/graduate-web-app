from fastapi import FastAPI, Depends, HTTPException, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from cas import CASClient

from sqlalchemy.orm import Session
from database import engine, get_db
from models import User

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


SERVICE_URL = "https://bktp-gradpro-api.discovery.cs.vt.edu/"

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
def login(request: Request, response: Response):
    
    username = request.cookies.get("username")
    if username: # return user info
        # Ensure the response has the JSON content-type
        return JSONResponse(content={"message": "Logged in!"}, media_type="application/json")
    
    cas_ticket = request.query_params.get("ticket")
    if not cas_ticket:
        cas_login_url = cas_client.get_login_url()
        return JSONResponse(content={"redirect_url": cas_login_url}, media_type="application/json")
    
    (user, _, _) = cas_client.verify_ticket(cas_ticket)
    if not user:
        raise HTTPException(status_code=403, detail="Failed to verify ticket!")

    # Redirect to the web app
    web_app_url = "https://bktp-gradpro.discovery.cs.vt.edu/"
    response = JSONResponse(content={"redirect_url": web_app_url}, media_type="application/json")

    # Set cookie with the domain attribute for the parent domain
    # and ensure it is set for cross-origin requests (SameSite=None; Secure)
    response.set_cookie(key="username", value=user, domain=".discovery.cs.vt.edu", 
                        samesite="None", secure=True, httponly=True)
    return response

@app.get("/api/logout")
def logout(response: Response):
    cas_logout_url = cas_client.get_logout_url(SERVICE_URL)
    response.delete_cookie("username")
    return {"redirect_url": cas_logout_url}

@app.get("/api/testSQL")
def testSQL(response: Response, db: Session = Depends(get_db)):
    user = db.query(User).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

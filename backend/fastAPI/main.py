from fastapi import FastAPI, Depends, HTTPException, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from cas import CASClient

app = FastAPI()

origins = [
    "http://localhost:3000",  # Example frontend development server
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


SERVICE_URL = "http://localhost:8000"

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
    if username:
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

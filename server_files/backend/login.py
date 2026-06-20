from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import sys
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
app = FastAPI()
from server_files.backend.db import check_user 

class user(BaseModel):
    username :str

@app.get("/")
def get():
    return FileResponse(BASE_DIR/"frontend/login.html")

@app.post("/click")
def click(username,password):
    return {"jaya":"hello"}
    if check_user(username) or correct_pass(username,password):
        return {"response":"logged in successfully"}
    return {"response":"incorrect username or password"}

@app.get("/forgot_password")
def get():
    return FileResponse(BASE_DIR/"frontend/forgot_password.html")

@app.post("/forgot_password")
def change_password(User:user):
    if check_user(User.username):
        #process to send email
        print(user.usrename)
        pass
    return {"response":"if email exists a recovery mail has been sent"}
    

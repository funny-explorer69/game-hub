from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
app = FastAPI()
import server_files.backend.db 

@app.get("/")
def get():
    return FileResponse(BASE_DIR/"frontend/login.html")

@app.post("/click")
def click(username,password):
    return {"jaya":"hello"}
    if check_user(username) or correct_pass(username,password):
        return {"response":"logged in successfully"}
    return {"response":"incorrect username or password"}

@app.post("/forgot_password/{username}")
def change_password(username):
    if check_user(username):
        #process to send email
        print("well done")
        pass
    return {"response":"if email exists a recovery mail has been sent"}
    

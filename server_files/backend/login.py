from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
app = FastAPI()

@app.get("/")
def get():
    return FileResponse(FRONTEND_DIR / "login.html")

@app.get("/click")
def click():
    return {"jaya":"hello"}
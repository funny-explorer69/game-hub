import sqlite3
from pathlib import Path
def get_connection():
    direc = Path(__file__).resolve().parent.parent
    db_path = direc / "database" / "users.db"
    conn = sqlite3.connect(db_path)
    return conn
def add_user(username,):
    if result:
        return {"response":"user with that username already exists"}
    pass
def check_user(username): # should check if user exists in database
    return True # -- testing --
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM USERS WHERE USERNAME = ?""",(username,)
    )
    result = cursor.fetchone()
    if result != None:
        return True
    return False
def correct_pass(username,password): # should check if the hash is same as in db
    pass
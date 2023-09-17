from ..config import *
from flask import session

def login(uid: int) -> dict:
    if session.get("logged_in"):
        JSONError.status_code = 409
        return JSONError.throw_json_error(error="Already logged in")
    
    session["logged_in"] = True
    session["valid_uid"] = uid
    return {
        "status": "ok",
        "message": "logged in successfully"
    }
    
    
def logout() -> dict:
    if not session.get("logged_in"):
        JSONError.status_code = 409
        return JSONError.throw_json_error(error="Already logged out")
    
    session["logged_in"] = False
    return {
        "status": "ok",
        "message": "logged out successfully"
    }
    
    
def get_session() -> dict:
    return {
        "status": "ok",
        "session": dict(session),
    }
from ..config import *
import datetime

class Application:
    conn: DBConnection = None
    
    aid: int = None
    uid: int = None
    pid: int = None
    
    status: int = None
    created_at: datetime = None
    updated_at: datetime = None
    resume_url: str = None
    cover_letter_url: str = None
    
    title: str = None
    description: str = None
    date: datetime = None
    field: str = None
    position: str = None
    wage: float = None
    job_start: datetime = None
    
    company_name: str = None
    industry: str = None
    website: str = None
    phone: str = None
    
    
    def __init__(self, aid = None):
        self.conn = DBConnection()
   
            
        
    def get(self, aid = None):
        pass
        
        
    def update_edit_timestamp(self):
        pass
    
    
    def update(self, keep_updated_at = False):
        pass
    
    
    def save(self):
        pass
    
    
    def delete(self):
        pass

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool = True
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)
    user_agent: Optional[str] = None
    submission_id: Optional[str] = None 

class StoredSurveyRecord(BaseModel):
     name: str
     email: str
     age: str
     consent: bool
     rating: int
     comments: Optional[str] = None
     source: str
     user_agent: Optional[str] = None
     submission_id: str
     received_at: datatime
     ip: str
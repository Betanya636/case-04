from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)

    consent: Optional[bool] = None
    rating: Optional[int] = None
    feedback: Optional[str] = None

    user_agent: Optional[str] = None
    submission_id: Optional[str] = None
e 

class StoredSurveyRecord(BaseModel):
     name: str
     email: str
     age: str
     consent: bool
     rating: int
     feedback: Optional[str] = None
     source: str
     user_agent: Optional[str] = None
     submission_id: str
     received_at: datatime
     ip: str
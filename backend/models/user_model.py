from typing import List, Optional
from pydantic import BaseModel # type: ignore

# 🔹 Each topic
class Topic(BaseModel):
    name: str
    difficulty: int   # 1–5
    confidence: int   # 1–5
    
    last_studied: Optional[str] = None
    next_revision: Optional[str] = None


# 🔹 Each subject contains topics
class Subject(BaseModel):
    name: str
    topics: List[Topic]


# 🔹 Full user profile
class User(BaseModel):
    name: str
    exam_date: str
    daily_hours: int
    subjects: List[Subject]
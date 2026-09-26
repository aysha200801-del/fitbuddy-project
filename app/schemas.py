from typing import Literal
from pydantic import BaseModel, Field

class UserInput(BaseModel):
    username: str = Field(min_length=1, max_length=120)
    user_id: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, lt=400)
    goal: Literal["weight loss", "muscle gain", "general wellness"]
    intensity: Literal["low", "medium", "high"]

class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str = Field(min_length=3, max_length=2000)

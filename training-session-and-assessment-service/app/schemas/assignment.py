from datetime import date
from typing import List, Optional

from app.schemas import training_session
from pydantic import BaseModel, Field


class ShowAssignment(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    session: training_session.ShowTrainingSessionFew
    given_date: date
    due_date: date
    total_score: float
    passing_score: float

    class Config:
        orm_mode = True


class ShowAssignmentList(BaseModel):
    assignments: List[ShowAssignment]
    skip: int
    limit: int


class CreateAssignment(BaseModel):
    title: str
    description: Optional[str] = None
    related_session: int
    given_date: date
    due_date: date
    total_score: float = Field(description="Total score should be greater than 0", gt=0)
    passing_score: float = Field(
        description="Passing score should be greater than 0", gt=0
    )


class UpdateAssignment(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    related_session: Optional[int] = None
    given_date: Optional[date] = None
    due_date: Optional[date] = None
    total_score: Optional[float] = Field(
        description="Total score should be greater than 0", gt=0
    )
    passing_score: Optional[float] = Field(
        description="Passing score should be greater than 0", gt=0
    )

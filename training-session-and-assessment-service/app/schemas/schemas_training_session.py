from datetime import date, datetime
from typing import List, Optional

from app.schemas.schemas_user import ShowUser
from pydantic import BaseModel, Extra


class ShowAssignmentFew(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    given_date: date
    due_date: date
    total_score: float
    passing_score: float

    class Config:
        orm_mode = True


class ShowTrainingSession(BaseModel):
    id: int
    topic: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_time: Optional[int] = None
    presenter: ShowUser
    recording_link: Optional[str] = None
    comment: Optional[str] = None
    expected_attendees: Optional[int] = None
    present_attendees: Optional[int] = None
    attendees: List[ShowUser]
    training_assignment: List[ShowAssignmentFew]

    class Config:
        orm_mode = True


class ShowTrainingSessionFew(BaseModel):
    id: int
    topic: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_time: Optional[int] = None
    recording_link: Optional[str] = None
    comment: Optional[str] = None
    expected_attendees: Optional[int] = None
    present_attendees: Optional[int] = None

    class Config:
        orm_mode = True


class ShowTrainingSessionList(BaseModel):
    training_session: List[ShowTrainingSession]
    skip: int
    limit: int


class CreateTrainingSession(BaseModel):
    topic: str
    start_time: datetime
    end_time: datetime
    user_fk: int
    comment: Optional[str] = None
    expected_attendees: Optional[int] = None
    attendees: List[int] = []

    class Config:
        extra = Extra.allow


class UpdateTrainingSession(BaseModel):
    topic: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_time: Optional[int] = None
    user_fk: Optional[int] = None
    recording_link: Optional[str] = None
    comment: Optional[str] = None
    expected_attendees: Optional[int] = None
    attendees: List[int] = []

    class Config:
        extra = Extra.allow

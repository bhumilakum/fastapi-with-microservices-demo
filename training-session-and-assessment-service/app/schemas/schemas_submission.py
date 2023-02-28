from datetime import date
from typing import List, Optional

from app.schemas.enums import SubmissionResultEnum
from app.schemas.schemas_assignment import ShowAssignmentFew
from app.schemas.schemas_user import ShowUser
from pydantic import BaseModel, Extra


class ShowGrade(BaseModel):
    knowledge: Optional[float] = None
    body_language: Optional[float] = None
    confidence: Optional[float] = None
    making_us_understand: Optional[float] = None
    practical: Optional[float] = None

    class Config:
        orm_mode = True


class ShowSubmission(BaseModel):
    id: int
    trainee_user: ShowUser
    trainee_assignment: ShowAssignmentFew
    submission_detail: str
    submission_date: date
    obtained_score: Optional[float] = None
    result: Optional[SubmissionResultEnum] = None
    submission_comment: Optional[str] = None
    mentor_remarks: Optional[str] = None
    submission_grade: Optional[ShowGrade] = None

    class Config:
        orm_mode = True


class ShowSubmissionList(BaseModel):
    submissions: List[ShowSubmission]
    skip: int
    limit: int


class ShowSubmissionFew(BaseModel):
    id: int
    submission_detail: str
    submission_date: date
    obtained_score: Optional[float] = None
    result: Optional[SubmissionResultEnum] = None
    submission_comment: Optional[str] = None
    mentor_remarks: Optional[str] = None
    trainee_assignment: ShowAssignmentFew
    submission_grade: Optional[ShowGrade] = None

    class Config:
        orm_mode = True


class ShowTraineeSubmissionList(BaseModel):
    submissions: List[ShowSubmissionFew]
    skip: int
    limit: int


class CreateSubmission(BaseModel):
    assignment_fk: int
    submission_detail: str
    submission_comment: Optional[str] = None

    class Config:
        extra = Extra.allow


class Grade(BaseModel):
    knowledge: float
    body_language: float
    confidence: float
    making_us_understand: float
    practical: float

    class Config:
        orm_mode = True


class UpdateSubmission(BaseModel):
    mentor_remarks: Optional[str] = None
    submission_grade: Optional[Grade] = None

    class Config:
        extra = Extra.allow
        orm_mode = True


class UpdateTraineeSubmission(BaseModel):
    assignment_fk: Optional[int] = None
    submission_detail: Optional[str] = None
    submission_comment: Optional[str] = None

    class Config:
        orm_mode = True

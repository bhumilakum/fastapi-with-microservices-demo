from app.core.database import Base
from app.schemas.enums import SubmissionResultEnum, UserTypeEnum
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.orm import relationship

# model to store M2M data for training session and user to manage user attendence
session_attendee = Table(
    "session_attendee",
    Base.metadata,
    Column(
        "session_id", Integer(), ForeignKey("training_session.id", ondelete="SET NULL")
    ),
    Column("user_id", Integer(), ForeignKey("users.id", ondelete="SET NULL")),
)


# The common fields that needs to be used in all the model
class BaseColumn(object):
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(
        DateTime, server_default=func.now(), onupdate=func.current_timestamp()
    )


class User(Base, BaseColumn):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    user_type = Column(Enum(UserTypeEnum), default=UserTypeEnum.mentor, nullable=False)

    training_sessions = relationship("TrainingSession", back_populates="presenter")
    submission_user = relationship("Submission", back_populates="trainee_user")


class TrainingSession(Base, BaseColumn):
    __tablename__ = "training_session"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_time = Column(Integer)
    user_fk = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    recording_link = Column(String)
    comment = Column(String)
    expected_attendees = Column(Integer)
    present_attendees = Column(Integer)

    attendees = relationship(
        "User", secondary=session_attendee, backref="training_session"
    )
    presenter = relationship("User", back_populates="training_sessions")
    training_assignment = relationship("Assignment", back_populates="session")


class Assignment(Base, BaseColumn):
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    related_session = Column(
        Integer, ForeignKey("training_session.id", ondelete="SET NULL")
    )
    given_date = Column(Date)
    due_date = Column(Date)
    total_score = Column(Float)
    passing_score = Column(Float)

    session = relationship("TrainingSession", back_populates="training_assignment")
    trainee_score = relationship("Submission", back_populates="trainee_assignment")


class Submission(Base, BaseColumn):
    __tablename__ = "submission"

    id = Column(Integer, primary_key=True, index=True)
    user_fk = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    assignment_fk = Column(Integer, ForeignKey("assignment.id", ondelete="SET NULL"))
    submission_detail = Column(String)
    submission_date = Column(Date)
    obtained_score = Column(Float)
    result = Column(Enum(SubmissionResultEnum), nullable=True)
    submission_comment = Column(String)
    mentor_remarks = Column(String)

    trainee_user = relationship("User", back_populates="submission_user")
    trainee_assignment = relationship("Assignment", back_populates="trainee_score")
    submission_grade = relationship(
        "Grade", uselist=False, back_populates="related_submission"
    )


class Grade(Base, BaseColumn):
    __tablename__ = "grade"

    id = Column(Integer, primary_key=True, index=True)
    submission_fk = Column(Integer, ForeignKey("submission.id", ondelete="SET NULL"))
    knowledge = Column(Float)
    body_language = Column(Float)
    confidence = Column(Float)
    making_us_understand = Column(Float)
    practical = Column(Float)

    related_submission = relationship("Submission", back_populates="submission_grade")

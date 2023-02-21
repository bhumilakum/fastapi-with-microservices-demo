from app.core.database import Base
from app.schemas.enums import GradePatternEnum, UserTypeEnum
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
)
from sqlalchemy.orm import relationship

session_attendee = Table(
    "session_attendee",
    Base.metadata,
    Column("session_id", Integer(), ForeignKey("training_session.id")),
    Column("user_id", Integer(), ForeignKey("users.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    user_type = Column(Enum(UserTypeEnum), default=UserTypeEnum.mentor, nullable=False)

    training_sessions = relationship("TrainingSession", back_populates="presenter")


class TrainingSession(Base):
    __tablename__ = "training_session"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_time = Column(Integer)
    user_fk = Column(Integer, ForeignKey("users.id"))
    recording_link = Column(String)
    comment = Column(String)
    expected_attendees = Column(Integer)
    present_attendees = Column(Integer)

    attendees = relationship(
        "User", secondary=session_attendee, backref="training_session"
    )
    presenter = relationship("User", back_populates="training_sessions")
    training_assignment = relationship("Assignment", back_populates="session")


class Assignment(Base):
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    related_session = Column(Integer, ForeignKey("training_session.id"))
    given_date = Column(Date)
    due_date = Column(Date)
    total_score = Column(Float)
    passing_score = Column(Float)

    session = relationship("TrainingSession", back_populates="training_assignment")
    trainee_score = relationship("Grade", back_populates="trainee_assignment")


class Grade(Base):
    __tablename__ = "grade"

    id = Column(Integer, primary_key=True, index=True)
    user_fk = Column(Integer, ForeignKey("users.id"))
    assignment_fk = Column(Integer, ForeignKey("assignment.id"))
    total_score = Column(Float)
    result = Column(String)
    comment = Column(String)

    trainee_assignment = relationship("Assignment", back_populates="trainee_score")
    grade_topic = relationship("GradePattern", back_populates="trainee_grade")


class GradePattern(Base):
    __tablename__ = "grade_pattern"

    id = Column(Integer, primary_key=True, index=True)
    grade_fk = Column(Integer, ForeignKey("grade.id"))
    grade_type = Column(
        Enum(GradePatternEnum), default=GradePatternEnum.knowledge, nullable=True
    )
    score = Column(Float)

    trainee_grade = relationship("Grade", back_populates="grade_topic")

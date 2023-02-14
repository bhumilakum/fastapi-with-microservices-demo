from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table, Date, DateTime, Float
from core.database import Base
from sqlalchemy.orm import relationship
import  enum


class UserTypeEnum(enum.Enum):
    admin = "admin"
    mentor = "mentor"
    trainee = "trainee"


session_attendee = Table(
    "session_attendee",
    Base.metadata,
    Column("session_id", Integer(), ForeignKey("training_session.id")),
    Column("user_id", Integer(), ForeignKey("user.id"))
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    user_type = Column(Enum(UserTypeEnum), default=UserTypeEnum.mentor, nullable=False)
    
    training_sessions = relationship("TrainingSession", back_populates="presenter")


class TrainingSession(Base):
    __tablename__ = 'training_session'

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_time = Column(Integer)
    user_fk = Column(Integer, ForeignKey('user.id'))
    recording_link = Column(String)
    attendence_link = Column(String)
    expected_attendees = Column(Integer)
    present_attendees = Column(Integer)

    attendees = relationship("User", secondary=session_attendee, backref="training_session")
    presenter = relationship("User", back_populates="training_sessions")
    training_assignment = relationship("Assignment", back_populates="session")


class Assignment(Base):
    __tablename__ = "assignment"
 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    related_session = Column(Integer, ForeignKey('training_session.id'))
    given_date = Column(Date)
    due_date = Column(Date)
    total_score = Column(Float)
    passing_score = Column(Float)

    session = relationship("TrainingSession", back_populates="training_assignment")
    trainee_score = relationship("Grade", back_populates="trainee_assignment")


class Grade(Base):
    __tablename__ = "grade"

    id = Column(Integer, primary_key=True, index=True)
    user_fk = Column(Integer, ForeignKey('user.id'))
    assignment_fk = Column(Integer, ForeignKey("assignment.id"))
    grade = Column(Float)
    result = Column(String)

    trainee_assignment = relationship("Assignment", back_populates="trainee_score")
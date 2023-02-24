import enum


class UserTypeEnum(enum.Enum):
    admin = "admin"
    mentor = "mentor"
    trainee = "trainee"


class GradePatternEnum(enum.Enum):
    knowledge = "knowledge"
    body_language = "body_language"
    confidence = "confidence"
    making_us_understand = "making_us_understand"
    practical = "practical"


class TrainingSessionFilter(str, enum.Enum):
    today = "today"
    past = "past"
    upcoming = "upcoming"
    my_sessions = "my_sessions"


class AssignmentFilter(str, enum.Enum):
    added_today = "added_today"
    due_today = "due_today"
    submitted_today = "submitted_today"
    my_submission = "my_submission"
    pending_submission = "pending_submission"
    due_submission = "due_submission"

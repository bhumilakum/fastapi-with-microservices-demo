import enum


class UserTypeEnum(enum.Enum):
    """
    UserType for the application users
    """

    admin = "admin"
    mentor = "mentor"
    trainee = "trainee"


class TrainingSessionFilter(str, enum.Enum):
    """
    Training Session filter options
    """

    today = "today"
    past = "past"
    upcoming = "upcoming"
    my_sessions = "my_sessions"


class SubmissionFilter(str, enum.Enum):
    """
    Assignment Submission filter options
    """

    submitted_today = "submitted_today"
    graded_submission = "graded_submission"
    pending_to_grade = "pending_to_grade"
    submission_result_PASS = "submission_result_PASS"
    submission_result_FAIL = "submission_result_FAIL"


class SubmissionResultEnum(enum.Enum):
    """
    Trinee score result filter options
    """

    PASS = "pass"
    FAIL = "fail"


class AssignmentFilter(str, enum.Enum):
    """
    Training Assignment filter options
    """

    submitted_assignment = "submitted_assignment"
    pending_assignment = "pending_assignment"
    due_assignment = "due_assignment"
    due_today = "due_today"

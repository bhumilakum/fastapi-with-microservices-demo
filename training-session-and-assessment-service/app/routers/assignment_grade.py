from fastapi import APIRouter

router = APIRouter(prefix="/assignment_grade", tags=["AssignmentGrade"])


@router.post("/logout")
def logout():
    pass

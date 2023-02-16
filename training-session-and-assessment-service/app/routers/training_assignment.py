from fastapi import APIRouter

router = APIRouter(prefix="/training_assignment", tags=["TrainingAssignments"])


@router.post("/logout")
def logout():
    pass

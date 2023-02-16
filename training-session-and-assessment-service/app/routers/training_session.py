from fastapi import APIRouter

router = APIRouter(prefix="/training_session", tags=["TrainingSessions"])


@router.post("/logout")
def logout():
    pass

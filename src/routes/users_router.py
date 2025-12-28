from fastapi import APIRouter


router = APIRouter(prefix="/users")


@router.post("/")
def register():
    pass


@router.post("/login")
def authenticate():
    pass


@router.get("/")
def get_current_user():
    pass


@router.put("/")
def update_current_user():
    pass

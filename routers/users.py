from fastapi import APIRouter
from sqlalchemy import text
from database import engine
from schemas import User

router = APIRouter()

@router.post("/register")
def register(user: User):

    return {
        "username": user.username,
        "email": user.email,
        "message": "User received successfully"
    }
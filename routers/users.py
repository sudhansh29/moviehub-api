from fastapi import APIRouter
from sqlalchemy import text
from database import engine
from schemas import User
from utils.security import hash_password

router = APIRouter()

@router.post("/register")
def register(user: User):
    with engine.connect() as conn:
        result = conn.execute(
        text("""
            SELECT id
            FROM users
            WHERE email = :email
        """),
        {
            "email": user.email
        }
    )
        existing_user = result.fetchone()

    if existing_user:
        return {"message":"Email already exists"}
    
    with engine.begin() as conn:
        conn.execute(
        text("""
            INSERT INTO users
            (username,email,password)

            VALUES
            (:username,:email,:password)
        """),
        {
            "username": user.username,
            "email": user.email,
            "password": hash_password(user.password)
        }
    )
        
    return {
    "message": "User registered successfully"}

    
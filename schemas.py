from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    genre: str

class User(BaseModel):
    username:str
    email:str
    password:str

class LoginUser(BaseModel):
    email:str
    password:str

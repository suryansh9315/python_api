from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    title: str
    content: str

class PostRes(BaseModel):
    id: int
    user_id: int
    title: str
    content: str

class AllPostRes(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    user_id: int
    email: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRes(BaseModel):
    id: int
    email: EmailStr

class Login(BaseModel):
    email: EmailStr
    password: str

class LoginRes(BaseModel):
    token: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Vote(BaseModel):
    post_id: int
    dir: int
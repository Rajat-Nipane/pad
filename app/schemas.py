from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint



class UserCreate(BaseModel):
    email : EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password: str

# inherting BaseModel from pydantic to validate the input
# class Post(BaseModel):
#     title: str
#     content: str
#     published : bool = True #default value

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True #default value

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at : datetime
    ownerr_id : int
    owner: UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dire : conint(le=1)


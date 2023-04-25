from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from . import utils
from typing import Optional,List
from random import randrange

import time
from . import models,schemas
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post,user,auth,votes

from .config import settings

from fastapi.middleware.cors import CORSMiddleware


# // no longer needed as we used alembic to reflect changes
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency




# my_posts = [
#     {
#     "id":1,
#     "title" : "Top Beaches in Florida",
#     "content" : "check out Florida and start with bithces",
#     "rating" : 5
#     },
#     {
#     "id":2,
#     "title" : "Beaches in Florida",
#     "content" : "bithces",
#     "rating" : 10
#     },
# ]

# def find_post(id):
#     for idx,p in enumerate(my_posts):
#         if p["id"] == id:
#             return  p,idx
#     idx = -1
#     p=None
#     return p ,idx

# path operations / route


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message":"Welcome Rajat!!!"}



# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data" : posts}


# Notes : 
# the below line is defined for sqlachemy
# db: Session = Depends(get_db)


from fastapi import APIRouter, Depends
from schemas.user_schema import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from typing import List

router = APIRouter(
    prefix = "/user",
    tags = ["user"]
)

#create a new user
@router.post("/", response_model=UserDisplay)
def create_user(request:UserBase, db : Session = Depends(get_db)):
    return db_user.create_user(db, request)

#read all users
@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)

#read user by id 
@router.get("/{user_id}", response_model=UserDisplay)
def get_user(user_id:int, db:Session=Depends(get_db)):
    return db_user.get_user(db, user_id)

#update a user by id 
@router.post("/{user_id}/update", response_model=UserDisplay)
def update_user(user_id:int, request:UserBase, db:Session=Depends(get_db)):
    return db_user.update_user(db, user_id, request)


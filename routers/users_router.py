from fastapi import APIRouter, Depends
from schemas.users_schema import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import users_controller
from typing import List

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

#create a new user
@router.post("/", response_model=UserDisplay)
def create_user(request:UserBase, db : Session = Depends(get_db)):
    return users_controller.create_user(db, request)

#read all users
@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return users_controller.get_all_users(db)

#read user by id 
@router.get("/{user_id}", response_model=UserDisplay)
def get_user(user_id:int, db:Session=Depends(get_db)):
    return users_controller.get_user(db, user_id)

#update a user by id 
@router.put("/{user_id}/update", response_model=UserDisplay)
def update_user(user_id:int, request:UserBase, db:Session=Depends(get_db)):
    return users_controller.update_user(db, user_id, request)

#delete a user by id 
@router.delete("/{user_id}/delete")
def delete(user_id:int, db:Session=Depends(get_db)):
    return users_controller.delete_user(db, user_id)



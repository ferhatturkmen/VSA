from fastapi import APIRouter, Depends
from schemas.users_schema import UserBase, UserCreate, UserDisplay, UserQuery, UserUpdateQuery
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import users_controller
from typing import List
from auth.oauth2 import oauth2_schema
from auth.oauth2 import get_current_user
from utils.user_utils import check_user, check_admin

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

#create a new user
@router.post("/", response_model=UserDisplay)
def create_user(request: UserCreate, 
                db: Session = Depends(get_db)):

    return users_controller.create_user(db, request)

#read all users
@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db), 
                  current_user:UserBase=Depends(get_current_user), 
                  query_params: UserQuery =  Depends()):
    check_admin(current_user)
    req_db_query = users_controller.get_all_users(db, query_params=query_params)
    return  req_db_query
       
    
#read user by id 
@router.get("/{user_id}", response_model=UserDisplay)
def get_user(user_id:int, 
             db:Session=Depends(get_db), 
             current_user:UserBase=Depends(get_current_user)):
    check_user(user_id, current_user)
    return users_controller.get_user(db, user_id)

#update a user by id 
@router.put("/{user_id}/update", response_model=UserDisplay)
def update_user(user_id:int, 
                request:UserUpdateQuery, 
                current_user:UserBase=Depends(get_current_user), 
                db:Session=Depends(get_db)):
    check_user(user_id, current_user)
    return users_controller.update_user(db, user_id, request, current_user)

#delete a user by id 
@router.delete("/{user_id}/delete")
def delete_user(user_id:int, 
                current_user:UserBase=Depends(get_current_user), 
                db:Session=Depends(get_db)):
    check_user(user_id, current_user)
    return users_controller.delete_user(db, user_id)



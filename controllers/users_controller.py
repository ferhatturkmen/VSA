from sqlalchemy.orm.session import Session
from schemas.users_schema import UserBase, UserQuery
from db.models import DbUser
from db.hash import Hash
from fastapi import HTTPException, status
from typing import Optional, List


def create_user (db:Session, request: UserBase ): 
    existing_user = db.query(DbUser).filter(DbUser.e_mail == request.e_mail).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"A user with the email address {request.e_mail} already exists.")
    new_user = DbUser(
        user_name = request.user_name,
        user_surname = request.user_surname,
        e_mail = request.e_mail,
        password = Hash.bcrypt(request.password),
        is_renter = request.is_renter,
        licence_type = request.licence_type,
        licence_date = str(request.licence_date) # check for change to date format
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session, query_params:  Optional[UserQuery] ):
     req_db_query = db.query(DbUser)
     if query_params:
            if query_params.user_name:
                req_db_query = req_db_query.filter(DbUser.user_name == query_params.user_name)
            if query_params.user_surname:
                req_db_query = req_db_query.filter(DbUser.user_surname == query_params.user_surname)
            if query_params.e_mail:
                req_db_query = req_db_query.filter(DbUser.e_mail == query_params.e_mail)
            if query_params.is_renter is not None:
                req_db_query = req_db_query.filter(DbUser.is_renter == query_params.is_renter)
            if query_params.licence_type:
                req_db_query = req_db_query.filter(DbUser.licence_type == query_params.licence_type)
            if query_params.licence_date:
                req_db_query = req_db_query.filter(DbUser.licence_date == query_params.licence_date)

     return req_db_query.all()



def get_user(db:Session, user_id:int):
    req_user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not req_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested user with id {user_id} is not found')
    return req_user

def get_user_by_email(db:Session, e_mail:str ):
    req_user = db.query(DbUser).filter(DbUser.e_mail == e_mail).first()
    if not req_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User with email address {e_mail} is not found')
    return req_user

def update_user(db:Session, user_id:int, request:UserBase):
     req_user= db.query(DbUser).filter(DbUser.user_id == user_id).first()
     if not req_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested user with id {user_id} is not found')
     else:
        req_user.user_name = request.user_name
        req_user.user_surname = request.user_surname
        req_user.e_mail = request.e_mail
        req_user.password = Hash.bcrypt(request.password)
        req_user.is_renter = request.is_renter
        req_user.licence_type = request.licence_type
        req_user.licence_date = request.licence_date    
     db.commit()
     db.refresh(req_user)
     return req_user

def delete_user(db:Session, user_id:int):
    req_user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not req_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested user with id {user_id} is not found')
    else:
        db.delete(req_user)
        db.commit()
    return f"User with id {user_id} is deleted"

     
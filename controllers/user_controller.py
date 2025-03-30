from sqlalchemy.orm.session import Session
from schemas.user_schema import UserBase
from db.models import DbUser
from db.hash import Hash
from fastapi import HTTPException, status


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
        licence_date = str(request.licence_date)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
     return db.query(DbUser).all()


def get_user(db:Session, user_id:int):
    req_user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not req_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested user with id {user_id} is not found')
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

     
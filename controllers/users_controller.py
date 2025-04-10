from sqlalchemy.orm.session import Session
from schemas.users_schema import UserBase, UserQuery, UserCreate, UserUpdateQuery, CurrentUserDisplay
from db.models import DbUser
from db.hash import Hash
from fastapi import HTTPException, status
from typing import Optional, List
from fastapi.responses import JSONResponse



def create_user (db:Session, 
                 request: UserCreate): 
    try:
        existing_user = db.query(DbUser).filter(DbUser.e_mail == request.e_mail).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"A user with the email address {request.e_mail} already exists.")
        new_user = DbUser(
            name = request.name,
            surname = request.surname,
            e_mail = request.e_mail,
            password = Hash.bcrypt(request.password),
            is_owner = False,
            is_admin = False,
            licence_type = request.licence_type,
            licence_date = request.licence_date 
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": f"User with email {request.e_mail} is created",
                     "user_id": new_user.user_id}
        )
    except HTTPException as e:
        raise e
    except Exception as e:       
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while creating user"
        )

def get_all_users(db: Session, query_params:  Optional[UserQuery] ):
    try:
        req_db_query = db.query(DbUser)
        if query_params:
            if query_params.name:
                req_db_query = req_db_query.filter(DbUser.name == query_params.name)
            if query_params.surname:
                req_db_query = req_db_query.filter(DbUser.surname == query_params.surname)
            if query_params.e_mail:
                req_db_query = req_db_query.filter(DbUser.e_mail == query_params.e_mail)
            if query_params.is_owner is not None:
                req_db_query = req_db_query.filter(DbUser.is_owner == query_params.is_owner)
            if query_params.licence_type:
                req_db_query = req_db_query.filter(DbUser.licence_type == query_params.licence_type)
            if query_params.licence_date:
                req_db_query = req_db_query.filter(DbUser.licence_date == query_params.licence_date)
        return req_db_query.all()
    
    except HTTPException as e:
        raise e
    except Exception as e:       
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while getting users"
        )



def get_user(db:Session, user_id:int):
    try:
        req_user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
        if not req_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Requested user with id {user_id} is not found')
        return req_user
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while getting user"
        )

def get_user_by_email(db:Session, e_mail:str ):
    try:
        req_user = db.query(DbUser).filter(DbUser.e_mail == e_mail).first()
        if not req_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with email address {e_mail} is not found')
        return req_user
    except HTTPException as e:
        raise e
    except Exception as e:       
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while getting user"
        )

def update_user(db:Session, user_id:int, request:UserUpdateQuery, current_user:CurrentUserDisplay):
    try:
        req_user= db.query(DbUser).filter(DbUser.user_id == user_id).first()
        if not req_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Requested user with id {user_id} is not found')
        
        if request.name is not None:
            req_user.name = request.name
        if request.surname is not None:
            req_user.surname = request.surname
        if request.e_mail is not None:
            req_user.e_mail = request.e_mail
        if request.password is not None:
            req_user.password = Hash.bcrypt(request.password)
     #   if request.is_owner is not None:
      #      req_user.is_owner = request.is_owner
        if request.licence_type is not None:
            req_user.licence_type = request.licence_type
        if request.licence_date is not None:
            req_user.licence_date = request.licence_date
        if request.is_admin is not None and current_user.is_admin:
            req_user.is_admin = request.is_admin  
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not authorized to update user admin status")  
        db.commit()
        db.refresh(req_user)
        return req_user
    
    except HTTPException as e:
        raise e
    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while updating user"
        )

def delete_user(db:Session, user_id:int):
    try:
        req_user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
        print (req_user.__dict__)
        if not req_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Requested user with id {user_id} is not found')
        
        db.delete(req_user)
        db.commit()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                            content={})
    
    except HTTPException as e:        
        raise e
    except Exception as e:        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Exception occured while deleting user"
        )

     
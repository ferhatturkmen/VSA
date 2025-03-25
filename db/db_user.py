from sqlalchemy.orm.session import Session
from schemas.user_schema import UserBase
from db.models import DbUser
from db.hash import Hash


def create_user (db:Session, request: UserBase ): 
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
     return db.query(DbUser).filter(DbUser.user_id == user_id).first()

def update_user(db:Session, user_id:int, request:UserBase):
     user= db.query(DbUser).filter(DbUser.user_id == user_id)
     user.update({
        DbUser.user_name: request.user_name,
        DbUser.user_surname:request.user_surname,
        DbUser.e_mail :request.e_mail,
        DbUser.password :Hash.bcrypt(request.password),
        DbUser.is_renter : request.is_renter,
        DbUser.licence_type : request.licence_type,
        DbUser.licence_date : request.licence_date
    })
     db.commit()
     return user_id
     
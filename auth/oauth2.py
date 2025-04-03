from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status, Depends
from controllers import users_controller
 
 
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
 
SECRET_KEY = '5090091c1e0fa881e7de3f97ccd45802a4f9703ab1ef1fa0e64fff9e870d3aca'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_current_user(token:str = Depends(oauth2_schema), db:Session=Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"www-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    e_mail: str= payload.get("sub")
    if e_mail is None:
      raise credentials_exception
  except jwt.JWTError:
    raise credentials_exception

  req_user = users_controller.get_user_by_email(db, e_mail)
  if req_user is None:
    raise credentials_exception
  
  return req_user
  



from schemas.users_schema import UserBase
from fastapi import HTTPException
def check_user(user_id:int, current_user:UserBase):
  if user_id != current_user.user_id:
       raise HTTPException(status_code=403, detail="You are not authorized to access this user.")
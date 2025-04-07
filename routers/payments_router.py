from fastapi import APIRouter, Depends
from schemas.payments_schema import PaymentBase, PaymentDisplay
from schemas.users_schema import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import payments_controller
from typing import List
from auth.oauth2 import oauth2_schema
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix = "/payments",
    tags = ["payments"]
)

#create a new payment request
@router.post("/new", response_model=PaymentDisplay)
def create_payment(request:PaymentBase, db : Session = Depends(get_db)):
    return payments_controller.create_payment_request(db, request)

#read all payments
@router.get("/all",) 
def get_all_payments(db: Session = Depends(get_db), 
                    current_user:UserBase=Depends(get_current_user),
                    query_params: PaymentBase =  Depends()):
    req_db_query = payments_controller.get_all_payments(db, query_params=query_params)
    return {
        "data": req_db_query ,
        "current_user": current_user
    }

#read payment by id 
@router.get("/{payment_id}", response_model=PaymentDisplay)
def get_payment(payment_id:int, db:Session=Depends(get_db), token:str = Depends(oauth2_schema)):
    return payments_controller.get_payment(db, payment_id)

#update a payment by id 
@router.put("/{payment_id}/update", response_model=PaymentDisplay)
def update_payment(payment_id:int, request:PaymentBase, db:Session=Depends(get_db)):
    return payments_controller.update_payment(db, payment_id, request)

#delete a payment by id 
@router.delete("/{payment_id}/delete")
def delete_payment(payment_id:int, db:Session=Depends(get_db)):
    return payments_controller.delete_payment(db, payment_id)



from fastapi import APIRouter, Depends
from schemas.payments_schema import PaymentBase, PaymentDisplay, PaymentQuery
from schemas.users_schema import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import payments_controller
from typing import List
from auth.oauth2 import oauth2_schema
from auth.oauth2 import get_current_user
from utils.user_utils import check_payer_reciever

router = APIRouter(
    prefix = "/payments",
    tags = ["payments"]
)

#create a new payment request
@router.post("/new", response_model=PaymentDisplay)
def create_payment(request:PaymentBase, 
                   current_user:UserBase=Depends(get_current_user),  
                   db: Session = Depends(get_db)):
    check_payer_reciever(request.booking_id, current_user, db)
    return payments_controller.create_payment_request(db, request)

#read all payments
@router.get("/all",) 
def get_all_payments(db: Session = Depends(get_db), 
                    current_user:UserBase=Depends(get_current_user),
                    query_params: PaymentQuery =  Depends()):
    req_db_query = payments_controller.get_all_payments(db, query_params=query_params)
    return {
        "data": req_db_query ,
        "current_user": current_user
    }

#read payment by id 
@router.get("/{payment_id}", response_model=PaymentDisplay)
def get_payment(payment_id:int, 
                db:Session=Depends(get_db), 
                current_user:UserBase=Depends(get_current_user)):
    check_payer_reciever(payment_id, current_user, db)
    return payments_controller.get_payment(db, payment_id)

#update a payment by id 
@router.put("/{payment_id}/update", response_model=PaymentDisplay)
def update_payment(payment_id:int, 
                   request:PaymentBase, 
                   current_user:UserBase=Depends(get_current_user),  
                   db:Session=Depends(get_db)):
    check_payer_reciever(payment_id, current_user, db)
    return payments_controller.update_payment(db, payment_id, request)

#delete a payment by id 
@router.delete("/{payment_id}/delete")
def delete_payment(payment_id:int, 
                   current_user:UserBase=Depends(get_current_user),  
                   db:Session=Depends(get_db)):
    check_payer_reciever(payment_id, current_user, db)
    return payments_controller.delete_payment(db, payment_id)



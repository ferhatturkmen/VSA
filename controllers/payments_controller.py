from sqlalchemy.orm.session import Session
from schemas.payments_schema import PaymentBase 
from db.models import db_payment
from fastapi import HTTPException, status
from typing import Optional


def create_payment_request (db:Session, request: PaymentBase ): 
    new_payment = db_payment(
        payment_amount = request.payment_amount,
        status = request.status,
        payment_approved_at = request.payment_approved_at,
        booking_id = request.booking_id
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment
 
def get_all_payments(db: Session, query_params: Optional[PaymentBase] ):
    req_db_query = db.query(db_payment)
    if query_params:
        if query_params.payment_amount:
            req_db_query = req_db_query.filter(db_payment.payment_amount == query_params.payment_amount)
        if query_params.status:
            req_db_query = req_db_query.filter(db_payment.status == query_params.status)
        if query_params.payment_approved_at:
            req_db_query = req_db_query.filter(db_payment.payment_approved_at == query_params.payment_approved_at)
        if query_params.booking_id:
            req_db_query = req_db_query.filter(db_payment.booking_id == query_params.booking_id)
    return req_db_query.all()

def get_payment(db:Session, payment_id:int):
    req_payment = db.query(db_payment).filter(db_payment.payment_id == payment_id).first()
    if not req_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested payment with id {payment_id} is not found')
    return req_payment


def update_payment(db: Session, payment_id: int, request: PaymentBase):
    req_payment = db.query(db_payment).filter(db_payment.payment_id == payment_id).first()
    if not req_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Requested payment with id {payment_id} is not found'
        )
    else:
        if request.payment_amount is not None:
            req_payment.payment_amount = request.payment_amount
        if request.status is not None:
            req_payment.status = request.status
        if request.payment_approved_at is not None:
            req_payment.payment_approved_at = request.payment_approved_at
        if request.booking_id is not None:
            req_payment.booking_id = request.booking_id
        db.commit()
        db.refresh(req_payment)
        return req_payment

def delete_payment(db:Session, payment_id:int):
    req_payment = db.query(db_payment).filter(db_payment.payment_id == payment_id).first()
    if not req_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested payment with id {payment_id} is not found')
    db.delete(req_payment)
    db.commit()
    return "Payment deleted successfully"
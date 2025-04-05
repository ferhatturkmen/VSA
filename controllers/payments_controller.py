from sqlalchemy.orm.session import Session
from schemas.payments_schema import PaymentBase 
from db.models import db_payment
from fastapi import HTTPException, status


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
 
def get_all_payments(db: Session):
    return db.query(db_payment).all()

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
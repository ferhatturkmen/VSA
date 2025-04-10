from sqlalchemy.orm.session import Session
from schemas.payments_schema import PaymentBase 
from db.models import db_payment
from fastapi import HTTPException, status
from typing import Optional
from fastapi.responses import JSONResponse


def create_payment_request (db:Session, request: PaymentBase ): 
    try:
        new_payment = db_payment(
            payment_amount = request.payment_amount,
            status = request.status,
            payment_approved_at = request.payment_approved_at,
            booking_id = request.booking_id
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": f"Payment with id {new_payment.payment_id} is created",
                     "payment_id": new_payment.payment_id,
                     "payment_amount": new_payment.payment_amount,
                     "status": new_payment.status,                     
                     "booking_id": new_payment.booking_id})
    except HTTPException as e:
        raise e
    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while creating payment"
        )
 
def get_all_payments(db: Session, query_params: Optional[PaymentBase] ):
    try:
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
    except HTTPException as e:
        raise e
    except Exception as e:        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while getting payments"
        )

def get_payment(db:Session, payment_id:int):
    try:
        req_payment = db.query(db_payment).filter(db_payment.payment_id == payment_id).first()
        if not req_payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Requested payment with id {payment_id} is not found')
        return req_payment
    except HTTPException as e:
        raise e
    except Exception as e:  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while getting payment"
        )


def update_payment(db: Session, payment_id: int, request: PaymentBase):
    try:
        req_payment = db.query(db_payment).filter(db_payment.payment_id == payment_id).first()
        if not req_payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Requested payment with id {payment_id} is not found'
            )
        
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
    except HTTPException as e:
        raise e
    except Exception as e:      
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while updating payment"
        )

def delete_payment(db:Session, payment_id:int):
    try:
        req_payment = db.query(db_payment).filter(db_payment.payment_id == payment_id).first()
        if not req_payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Requested payment with id {payment_id} is not found')
        db.delete(req_payment)
        db.commit()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                            content={}) 
    
    except HTTPException as e:
        raise e
    except Exception as e:       
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while deleting payment"
        )
#from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean, TIMESTAMP, Float, DateTime
from db.database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, Float, DateTime


class DbUser(Base) :
    __tablename__ = "users"
    user_id = Column(Integer, primary_key = True, index = True)
    user_name = Column(String)
    user_surname = Column(String)
    e_mail = Column(String, unique=True, index=True)
    password = Column(String)
    is_renter = Column(Boolean, default=False)
    licence_type = Column(String)
    licence_date = Column(String)
   # created_at = Column(TIMESTAMP)
   

class db_vehicle(Base) :
    __tablename__ = "vehicles"
    vehicle_id =Column(Integer, primary_key=True, index=True)
    plate = Column(String, unique=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Date, nullable=False)
    fuel_type = Column(String, nullable=False)
    total_person = Column(Integer)
    is_commercial = Column(Boolean)
    room_size = Column(Float)
    is_automatic = Column(Boolean, nullable=False)
    include_listing = Column(Boolean, default=True)
    # !!! user_id add relation!!!!!!!!!!!!!!

class db_vehicle_property(Base) :
    __tablename__ = "vehicle_properties"
    property_id =Column(Integer, primary_key=True, index=True)
    daily_rate = Column(Float, nullable=False)
    location = Column(String, nullable=False, index=True)
    unavailable_dates = Column(String)
    # !!!!! vehicle id add relation !!!!!!!

class db_booking(Base) :
    __tablename__ = "bookings"
    booking_id =Column(Integer, primary_key=True, index=True)
    booking_date = Column(DateTime, nullable=False)
    total_days = Column(Integer)
    created_at = Column(TIMESTAMP)
    approved_at = Column(TIMESTAMP)
    is_delivered_up = Column(Boolean, default = False)
    damage_report = Column(String)
    is_report_approved = Column(Boolean, default=False)
    approved_at = Column(TIMESTAMP)
    is_cancelled = Column(Boolean, nullable=True)
    cancelled_at = Column(TIMESTAMP, nullable=True)
    cancellation_type = Column(String, nullable=True)    
    # !!! user_id renter add relation !!!!!!
    # !!!! user_id owner add relation !!!!!!!
    # !!!! vehicle_id add relation !!!!!


class db_payment(Base) :
    __tablename__ = "payments" 
    payment_id =Column(Integer, primary_key=True, index=True)
    payment_amount = Column(Float)
    deposit_amount = Column(Float)
    is_pending = Column(Boolean, default=True)
    payment_approved_at = Column(TIMESTAMP)    
    deposit_back_at = Column(TIMESTAMP)
    #booking_id add relation!!!!!
    # is_approved add relation !!!!










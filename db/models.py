#from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean, TIMESTAMP, Float, DateTime
from db.database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, Float, DateTime, func, Enum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class DbUser(Base) :
    __tablename__ = "users"
    user_id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    surname = Column(String)
    e_mail = Column(String, unique=True, index=True)
    password = Column(String)
    is_owner = Column(Boolean, default=False)
    licence_type = Column(Enum("A", "B", "C", "D", "E"), nullable=False)
    licence_date = Column(Date)
    is_admin = Column(Boolean, default=False)
    owned_vehicles= relationship("db_vehicle", back_populates="owner")
    rented_bookings = relationship("db_booking", foreign_keys="[db_booking.renter_id]", back_populates="renter")     


class db_vehicle(Base) :
    __tablename__ = "vehicles"
    vehicle_id =Column(Integer, primary_key=True, index=True)
    plate = Column(String, unique=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(String, nullable=False)
    fuel_type = Column(Enum("Benzine","Diesel", "Electric", "Hybrid", "LPG" ))
    total_person = Column(Integer)
    is_commercial = Column(Boolean)    
    is_automatic = Column(Boolean, nullable=False)
    navigation = Column(Boolean, default=False)
    air_condition = Column(Boolean, default=False)
    include_listing = Column(Boolean, default=True)
    daily_rate = Column(Float, nullable=False)
    location = Column(String, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    owner = relationship("DbUser", back_populates="owned_vehicles")   
    vehicle_rentings = relationship("db_booking", foreign_keys="[db_booking.rented_vehicle_id]", back_populates="rented_vehicle")
    vehicle_files = relationship("db_vehicle_files", back_populates="files")



class db_vehicle_files(Base) :
    __tablename__ = "vehicle_files"
    file_id =Column(Integer, primary_key=True, index=True)
    #filename = Column (String, nullable=True)
    file_url = Column(String, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id")) 
    files = relationship("db_vehicle", back_populates="vehicle_files")
  
class db_booking(Base) :
    __tablename__ = "bookings"
    booking_id =Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)   
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    is_delivered_up = Column(Boolean, default = False)
    damage_report = Column(String)
    is_report_approved = Column(Boolean, default=False)
    approved_at = Column(TIMESTAMP)
    is_cancelled = Column(Boolean, default=False)
    cancelled_at = Column(TIMESTAMP, nullable=True)  
    renter_id = Column(Integer, ForeignKey("users.user_id"))
    rented_vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id")) 
    renter = relationship("DbUser", back_populates="rented_bookings")
    rented_vehicle= relationship("db_vehicle", back_populates="vehicle_rentings")
    booking_payment = relationship("db_payment", uselist=False, back_populates="payment_belongs_to")
    booking_reviews = relationship("db_review", back_populates="review_belongs_to")
   
    
class db_payment(Base) :
    __tablename__ = "payments" 
    payment_id =Column(Integer, primary_key=True, index=True)
    payment_amount = Column(Float)
    status = Column(Enum("pending", "approved", "rejected" "cancelled",), default="pending") 
    payment_approved_at = Column(DateTime, nullable=True)        
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    payment_belongs_to = relationship("db_booking", back_populates="booking_payment")
    


class db_review(Base) :
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), index=True)
    review_type = Column(Enum("renterTOowner", "ownerTOrenter", "renterTOvehicle", nullable=False))
    review_rating = Column (Integer, nullable=False)
    review_belongs_to = relationship("db_booking", back_populates="booking_reviews") #db_review










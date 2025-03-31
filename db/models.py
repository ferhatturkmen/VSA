#from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean, TIMESTAMP, Float, DateTime
from db.database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, Float, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


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
    owned_vehicles= relationship("db_vehicle", back_populates="owner")
    rented_bookings = relationship("db_booking", foreign_keys="[db_booking.renter_id]", back_populates="renter")     


class db_vehicle(Base) :
    __tablename__ = "vehicles"
    vehicle_id =Column(Integer, primary_key=True, index=True)
    plate = Column(String, unique=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(String, nullable=False)
    fuel_type = Column(String, nullable=False)
    total_person = Column(Integer)
    is_commercial = Column(Boolean)
    room_size = Column(Float)
    is_automatic = Column(Boolean, nullable=False)
    navigation = Column(Boolean, default=False)
    air_condition = Column(Boolean, default=False)
    include_listing = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    owner = relationship("DbUser", back_populates="owned_vehicles")
    vehicle_properties = relationship("db_vehicle_property", back_populates="properties")
    vehicle_rentings = relationship("db_booking", foreign_keys="[db_booking.rented_vehicle_id]", back_populates="rented_vehicle")
    vehicle_images = relationship("db_vehicle_image", back_populates="images")

class db_vehicle_property(Base) :
    __tablename__ = "vehicle_properties"
    property_id =Column(Integer, primary_key=True, index=True)
    daily_rate = Column(Float, nullable=False)
    location = Column(String, nullable=False, index=True)
    unavailable_dates = Column(String)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id")) 
    properties = relationship("db_vehicle", back_populates="vehicle_properties")  

class db_vehicle_image(Base) :
    __tablename__ = "vehicle_images"
    image_id =Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id")) 
    images = relationship("db_vehicle", back_populates="vehicle_images")
  

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
    renter_id = Column(Integer, ForeignKey("users.user_id"))
    rented_vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id")) 
    renter = relationship("DbUser", back_populates="rented_bookings")
    rented_vehicle= relationship("db_vehicle", back_populates="vehicle_rentings")
   
    
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










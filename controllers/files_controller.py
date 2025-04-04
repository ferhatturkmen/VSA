from sqlalchemy.orm import Session
from db.models import db_vehicle, db_vehicle_image
from fastapi import HTTPException, status
import os


# Upload image to the vehicle
UPLOAD_FOLDER = r".\img" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def upload_vehicle_images(db: Session, vehicle_id: int, files: list):
    req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
    if not req_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Vehicle with id {vehicle_id} not found")
    
    image_paths = []   
    for file in files:  
              
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        #sanitized_filename = file.filename.replace(" ", "_")
        #file_location = os.path.join(UPLOAD_FOLDER, sanitized_filename)
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        
        add_image = db_vehicle_image(vehicle_id=vehicle_id, image_url=file_location)
        db.add(add_image)
        db.commit()
        db.refresh(add_image)
        image_paths.append(file_location)

        return "Image uploaded successfully!"






def get_images_by_car(db: Session, vehicle_id: int):
    
    car = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car with id {vehicle_id} not found")

    images = db.query(db_vehicle_image).filter(db_vehicle_image.vehicle_id == vehicle_id).all()
    
    if not images:
        raise HTTPException(status_code=404, detail="No images found for car with id {vehicle_id}")

    return images








#delete image from a vehicle

def delete_image(db: Session, image_id:int):
  image_to_delete = db.query(db_vehicle_image).filter(db_vehicle_image.image_id == image_id).first()
  if not image_to_delete:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Image with id {image_id} not found")
  db.delete(image_to_delete)
  db.commit()
  return "Image deleted successfully!"







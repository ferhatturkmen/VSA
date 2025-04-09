from sqlalchemy.orm import Session
from db.models import db_vehicle, db_vehicle_files
from fastapi import HTTPException, status
import os
from fastapi.responses import JSONResponse



# Upload files to the vehicle
UPLOAD_FOLDER = r".\files" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def upload_vehicle_file(db: Session, vehicle_id: int, files: list):
    req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
    if not req_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Vehicle with id {vehicle_id} not found")
    
    file_paths = []   
    for file in files:  
              
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        sanitized_filename = file.filename.replace(" ", "_")
        file_location = os.path.join(UPLOAD_FOLDER, sanitized_filename)
        #file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        
        add_file = db_vehicle_files(vehicle_id=vehicle_id, file_url=file_location)
        db.add(add_file)
        db.commit()
        db.refresh(add_file)
        file_paths.append(file_location)

        return "File uploaded successfully!"






def get_files_by_car(db: Session, vehicle_id: int):
    
    car = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
    if not car:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {vehicle_id} not found")

    images = db.query(db_vehicle_files).filter(db_vehicle_files.vehicle_id == vehicle_id).all()
    if not images:
        raise HTTPException(status_code=404, detail=f"No files found for vehicle with id {vehicle_id}")

    return images








#delete file from a vehicle

def delete_file(db: Session, file_id:int):
  file_to_delete = db.query(db_vehicle_files).filter(db_vehicle_files.file_id == file_id).first()
  if not file_to_delete:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"File with id {file_id} not found")
        
  db.delete(file_to_delete)
  db.commit()
  return JSONResponse(
        status_code=status.HTTP_204_DELETED,  
        content={"message": "File deleted successfully!"}
    )








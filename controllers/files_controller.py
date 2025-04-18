from sqlalchemy.orm import Session
from db.models import db_vehicle, db_vehicle_files
from fastapi import HTTPException, status, UploadFile, File
import os
from fastapi.responses import JSONResponse, Response
from auth.oauth2 import get_current_user
from schemas.users_schema import UserBase
#from typing import List



# Upload files to the vehicle
UPLOAD_FOLDER = r".\files" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#check if file has allowed extension
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png'}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    extension = os.path.splitext(filename)[1].lower() 
    return extension in ALLOWED_EXTENSIONS

# def upload_vehicle_file(db: Session, vehicle_id: int, files: UploadFile):
#         req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
#         if not req_vehicle:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                                 detail=f"Vehicle with id {vehicle_id} not found")
def upload_vehicle_file(db: Session, vehicle_id: int, file: UploadFile,current_user: UserBase):
    try:
      req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
      if not req_vehicle:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Vehicle with id {vehicle_id} not found")

       #Check ownership
      if req_vehicle.owner_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: No permition to change someone else's data"
            )
      
    # Process each file in the 'files' list
    
      if not allowed_file(file.filename):
              raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.filename} is not allowed. Allowed extensions are: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size (10 MB limit)
      file_size = len(file.file.read()) 
      file.file.seek(0) 
      if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File {file.filename} is too large. Maximum allowed size is 10 MB."
            )

      if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

      sanitized_filename = file.filename.replace(" ", "_")
      file_location = os.path.join(UPLOAD_FOLDER, sanitized_filename)

        # file saving to the specified location
      with open(file_location, "wb") as f:
            f.write(file.file.read())

        # file adding entry to the database
      add_file = db_vehicle_files(vehicle_id=vehicle_id, file_url=file_location)
      db.add(add_file)
      db.commit()
      db.refresh(add_file)

        # Append the file location to the file_paths list
        #file_paths.append(file_location)


    # Return a response after all files are processed
      return JSONResponse(
        status_code=201,
        content={
                 "file_paths": file_location
        }
      )
           
    except HTTPException as e:
        raise e
    except Exception as e:       
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured during adding file"
        )




#get all files related with vehicle

def get_files_by_car(db: Session, vehicle_id: int, ):
    try:    
        car = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail=f"Vehicle with id {vehicle_id} not found")

        images = db.query(db_vehicle_files).filter(db_vehicle_files.vehicle_id == vehicle_id).all()
        if not images:
            raise HTTPException(status_code=404, detail=f"No files found for vehicle with id {vehicle_id}")

        return images
    
    except HTTPException as e:
        raise e
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while getting image"
        )






#delete file from a vehicle

def delete_file(db: Session, file_id:int):
    try:
        file_to_delete = db.query(db_vehicle_files).filter(db_vehicle_files.file_id == file_id).first()

        if not file_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"File with id {file_id} not found")
            
        db.delete(file_to_delete)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception as e:        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception occured while deleting image"
        )






# #check if file has allowed extension
# ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png'}

# MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

# def allowed_file(filename: str) -> bool:
#     """Check if the file has an allowed extension."""
#     extension = os.path.splitext(filename)[1].lower() 
#     return extension in ALLOWED_EXTENSIONS

# def upload_vehicle_file(db: Session, vehicle_id: int, files: list[UploadFile]):
#     req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
#     if not req_vehicle:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"Vehicle with id {vehicle_id} not found")

#     file_paths = []     
#     # Process each file in the 'files' list
#     for file in files:
#         if not allowed_file(file.filename):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"File type {file.filename} is not allowed. Allowed extensions are: {', '.join(ALLOWED_EXTENSIONS)}"
#             )
        
#         # Check file size (10 MB limit)
#         file_size = len(file.file.read()) 
#         file.file.seek(0) 
#         if file_size > MAX_FILE_SIZE:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"File {file.filename} is too large. Maximum allowed size is 10 MB."
#             )

#         if not os.path.exists(UPLOAD_FOLDER):
#             os.makedirs(UPLOAD_FOLDER)

#         sanitized_filename = file.filename.replace(" ", "_")
#         file_location = os.path.join(UPLOAD_FOLDER, sanitized_filename)

#         # file saving to the specified location
#         with open(file_location, "wb") as f:
#             f.write(file.file.read())

#         # file adding entry to the database
#         add_file = db_vehicle_files(vehicle_id=vehicle_id, file_url=file_location)
#         db.add(add_file)
#         db.commit()
#         db.refresh(add_file)

#         # Append the file location to the file_paths list
#         file_paths.append(file_location)


#     # Return a response after all files are processed
#     return JSONResponse(
#         status_code=201,
#         content={
#             "message": "File uploaded successfully!",
#             "file_paths": file_paths
#         }
#     )
    
    # file_paths = []   
    # for file in files:  
              
    #     if not os.path.exists(UPLOAD_FOLDER):
    #         os.makedirs(UPLOAD_FOLDER)

    #     sanitized_filename = file.filename.replace(" ", "_")
    #     file_location = os.path.join(UPLOAD_FOLDER, sanitized_filename)
    #     #file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    #     with open(file_location, "wb") as f:
    #         f.write(file.file.read())
        
    #     add_file = db_vehicle_files(vehicle_id=vehicle_id, file_url=file_location)
    #     db.add(add_file)
    #     db.commit()
    #     db.refresh(add_file)
    #     file_paths.append(file_location)

    #     return JSONResponse(
    #       status_code=201,
    #       content={"message": "File uploaded successfully!"}
    #  )
       





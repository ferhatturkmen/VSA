from pydantic import BaseModel
from typing import Optional , List


class VehicleImageDisplay(BaseModel):
    image_id: int
    filename: Optional[str]
    image_url: Optional[str]
    vehicle_id: Optional[int] #don't forget to delete Optional
   

    class Config():
        from_attributes = True
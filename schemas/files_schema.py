from pydantic import BaseModel
from typing import Optional #, List


class VehicleFileDisplay(BaseModel):
    file_id: int
    file_url: Optional[str]
    vehicle_id: int 
   

    class Config():
        from_attributes = True
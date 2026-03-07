from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RoomCreate(BaseModel):
    name: Optional[str] = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    capacity: int  = Field(..., le=150)
    capacity_exam: int = Field(..., le=30)
    active: bool = Field(..., default=True)
    characteristic_name: str = Field(..., max_length=150)
    building_identifier: str = Field(..., max_length=50)

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    location: Optional[str] = Field(None, max_length=255)
    capacity: Optional[int] = Field(None, le=150)
    capacity_exam: Optional[int] = Field(None, le=30)
    active: Optional[bool] = Field(None, default=True)
    characteristic_name: Optional[str] = Field(None, max_length=150)
    building_identifier: Optional[str] = Field(None, max_length=50)




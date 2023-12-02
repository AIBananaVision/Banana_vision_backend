from pydantic import BaseModel
from enum import Enum
from typing import Optional
from bson import ObjectId
from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
        
class ContentTypeEnum(str, Enum):
    image = "image"
    video = "video"

class LocationData(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    countryName: Optional[str] = None
    locality: Optional[str] = None
    address: Optional[str] = None
    address: Optional[str] = None

class ImageUpload(BaseModel):
    image_url: str = None
    location: LocationData = None
    disease_class: str = "healthy"

 
    

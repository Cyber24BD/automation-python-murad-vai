from pydantic import BaseModel, Field
from typing import Optional, List

class ItemBase(BaseModel):
    name: str
    description: str
    price: str
    town_hall_level: str
    king_level: str
    queen_level: str
    warden_level: str
    champion_level: str
    media1: str
    media2: Optional[str] = None
    media3: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

# Schema for the nested media object in JSON uploads
class Media(BaseModel):
    media1: str
    media2: Optional[str] = None
    media3: Optional[str] = None

# Schema for validating a single item from a JSON upload
class ItemUpload(BaseModel):
    name: str
    description: str
    price: str
    town_hall_level: str = Field(..., alias='Town Hall Level')
    king_level: str = Field(..., alias='King Level')
    queen_level: str = Field(..., alias='Queen Level')
    warden_level: str = Field(..., alias='Warden Level')
    champion_level: str = Field(..., alias='Champion Level')
    media: Media


# Schemas for the public /json endpoint
class MediaOut(BaseModel):
    media1: Optional[str] = None
    media2: Optional[str] = None
    media3: Optional[str] = None

class ItemOut(BaseModel):
    name: str
    description: Optional[str] = None
    price: str
    town_hall_level: str = Field(alias="Town Hall Level")
    king_level: str = Field(alias="King Level")
    queen_level: str = Field(alias="Queen Level")
    warden_level: str = Field(alias="Warden Level")
    champion_level: str = Field(alias="Champion Level")
    media: Optional[MediaOut] = None

    class Config:
        from_attributes = True
        populate_by_name = True


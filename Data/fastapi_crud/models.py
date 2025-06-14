from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(String)
    town_hall_level = Column(String)
    king_level = Column(String)
    queen_level = Column(String)
    warden_level = Column(String)
    champion_level = Column(String)
    media = Column(JSON)

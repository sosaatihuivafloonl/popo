from sqlalchemy import Boolean, Column, Integer, String, MetaData, TIMESTAMP, ForeignKey, Table, CheckConstraint, DateTime
from database.connection import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship, declarative_base

metadata = MetaData()
Base = declarative_base()

class Cart(Base):
    __tablename__ = "data_info"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=False, index=True)
    product_id_url = Column(String, unique=False, index=True)
    target_username = Column(String, unique=False, index=True)
    target_photo_url = Column(String, unique=False, index=True)
    item_photo_url = Column(String, unique=False, index=True)
    item_name = Column(String, unique=False, index=True)
    item_price = Column(String, unique=False, index=True)
    


class MyResponse(BaseModel):
	request: str
	error: str


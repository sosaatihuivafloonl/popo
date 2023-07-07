from sqlalchemy import Boolean, Column, Integer, String, MetaData, TIMESTAMP, ForeignKey, Table, CheckConstraint, DateTime
from database.connection import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship, declarative_base
from fastapi import Form

metadata = MetaData()
Base = declarative_base()

class Cart(Base):
    __tablename__ = "data_info"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    product_id_url = Column(String, unique=False, index=True)
    target_username = Column(String, unique=False, index=True)
    target_photo_url = Column(String, unique=False, index=True)
    item_photo_url = Column(String, unique=False, index=True)
    item_name = Column(String, unique=False, index=True)
    item_price = Column(String, unique=False, index=True)
    


class CartRequestForm:
	
    def __init__(
        self,
        product_id: str = Form(),
        product_id_url: str = Form(),
        target_username: str = Form(),
        target_photo_url: str = Form(),
        item_photo_url: str = Form(),
        item_name: str = Form(),
        item_price: str = Form(),
    ):
        self.product_id = product_id
        self.product_id_url = product_id_url
        self.target_username = target_username
        self.target_photo_url = target_photo_url
        self.item_photo_url = item_photo_url
        self.item_name = item_name
        self.item_price = item_price
        



class MyResponse(BaseModel):
	request: str
	error: str


from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
	id: Optional[int]=None
	product_id: Optional[str]=None
	product_id_url: Optional[str]=None
	target_username: Optional[str]=None
	target_photo_url: Optional[str]=None
	item_photo_url: Optional[str]=None
	item_name: Optional[str]=None
	item_price: Optional[str]=None
 
	class Config:
		orm_mode = True
  

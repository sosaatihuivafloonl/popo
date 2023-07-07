from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.model import Cart
from models import model
from database.connection import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
import httpx
from config import BOT_TOKEN, CHAT_ID


model.Base.metadata.create_all(bind=engine)

# app = FastAPI(docs_url=None)
app = FastAPI()


origins = [	'http://localhost:3000', 
			'http://localhost:3001', 
			'http://localhost:3002', 
           	'https://carouseell.com',
           	'https://carouseell.store',
        	] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", 'GET'],
    allow_headers=["*"],
)



async def send_telegram_message(bot_token: str, chat_id: str, message: str ):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        
@app.post("/api/send_data")
async def send_message_to_telegram(message: str):
    await send_telegram_message(BOT_TOKEN, CHAT_ID, message)
    return {"status": "Message sent successfully"}

@app.get('/api/get_data')
def create_user(
    db: Session = Depends(get_db)
    ):
    all_data = db.query(Cart).all();
    return all_data;
    

@app.post("/api/fetch_user_data")
def create_user(
    db: Session = Depends(get_db),
    formData: model.CartRequestForm = Depends()
    ):
    try:
        existing_cart = db.query(Cart).filter_by(product_id=formData.product_id).first()
        if existing_cart:
            raise HTTPException(status_code=400, detail='product_id already exists')
        else:
            cartQuery = Cart(
				product_id=formData.product_id, 
				product_id_url=formData.product_id_url,
				target_username=formData.target_username,
				target_photo_url=formData.target_photo_url,
				item_photo_url=formData.item_photo_url,
				item_name=formData.item_name,
				item_price=formData.item_price,
				)
            db.add(cartQuery)
            db.commit()
            db.refresh(cartQuery)
            return cartQuery
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=e)
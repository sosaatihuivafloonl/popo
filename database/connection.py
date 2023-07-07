from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



DATABASE_URL = f"postgresql://car_uhzr_user:uMhpHmMYnLgLrOMTUS4kFR4eE6UxTJZz@dpg-cijk1th8g3nc2g9h2rag-a.frankfurt-postgres.render.com:5432/car_uhzr"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()













from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_extensive(db: Session,title:str,name:str,desc:str,url:str):
    db_extensive = models.Extensive(title=title,desc=desc,name=name,url=url)
    db.add(db_extensive)
    db.commit()
    db.refresh(db_extensive)
    return db_extensive

def get_extensive(db, id: int):
    return db.query(models.Extensive).filter(models.Extensive.id== id).first()

def extensive_list(db):
    return db.query(models.Extensive).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Extensive.__table__
   sym = sym1.delete().where(models.Extensive.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True
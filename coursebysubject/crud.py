from sqlalchemy.orm import Session
from . import models, schemas
from .schemas import SubjectBase,SubjectUpdate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import datetime

def create_subject(db: Session,title:str,name:str,desc:str,url:str):
    db_subject = models.Subject(title=title,desc=desc,name=name,url=url)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subject(db, id: int):
    return db.query(models.Subject).filter(models.Subject.id== id).first()

def subject_list(db):
    return db.query(models.Subject).all()
    
async def delete(db: Session,id: int)-> bool:
   sym1 =models.Subject.__table__
   sym = sym1.delete().where(models.Subject.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True

# async def update_subject(db: Session,title:str,name:str,desc:str,url:str,subject_id:int):
#     query = models.Subject.__table__.update()\
#     .where(models.Subject.id== subject_id)\
#     .values(title=title,desc=desc,name=name,url=url).returning(models.Subject.id)
#     #db_subjects = models.Subject(title=title,desc=desc,name=name,url=url)
#     # db.execute(db_subj)
#     # db.commit()
#     # db.refresh(db_subj)
#     # return db_subj
#     #return db.execute(query)
#     return True

async def update_subject(db: Session,
#title:str,name:str,desc:str,url:str,id=int,
 subject = schemas.SubjectBase):
    db_subject = db.query(models.Subject).filter(models.Subject.id == id).first()
    db_subject.title = subject.title
    db_subject.name = subject.name
    #db_subject.url = models.Subject.__table__.url
    db_subject.desc = subject.desc
    db.commit()
    db.refresh(db_subject)
    return await db_subject
# async def update_subject(db: Session,id: int, payload: SubjectUpdate):
#     query = (
#         models.Subject.__table__
#         .update()
#         .where(id == models.Subject.id)
#         .values(name=payload.name,title=payload.title,description=payload.desc)
#         .returning(models.Subject.id)
#     )
#     return await db.execute(query=query)
   
# async def put_sub(db: Session, id: int, subj :schemas.SubjectUpdate):
#     gdate = str(datetime.datetime.now())
#     query = models.Subject.__table__.update().\
#         where(models.Subject.id == id).\
#         values(
#         name = models.Subject.name,
#         title = models.Subject.title,
#         desc = models.Subject.desc,
#         #password = util.get_password_hash(user.password),#
#         #confirm_password =  util.get_password_hash(user.confirm_password),#
#         # first_name = user.first_name,
#         # last_name = user.last_name,
#         # dateofbirth = user.dateofbirth,
#         # phone = user.phone,
#         created_date = gdate,
#         )
#     db.execute(query)
#     db.commit()
#     return True
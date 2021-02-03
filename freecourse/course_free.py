from typing import Dict, List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
#from courses_live.database import SessionCourse, some_engine
from writer.database import SessionLocal, engine
import shutil
from freecourse.schemas import FreeBase, FreeUpdate
from freecourse.models import Free
import datetime
#from coursebysubject.models import subjects
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
router = APIRouter()


import uuid
from pathlib import Path
import time
#from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
import os
from os.path import dirname, abspath, join


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

router.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')

@router.post("/free/")
def create_free(
    title:str,desc:str,name:str,file: UploadFile= File(...), db: Session = Depends(get_db)
):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    with open("static/"+filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    #url = str("media/"+file.filename)
    url = os.path.join(images_path, filename)
    return crud.create_free(db=db,name=name,title=title,desc=desc,url=url)

@router.get("/frees/"  ,dependencies=[Depends(pagination_params)])
def free_list(db: Session = Depends(get_db)):
    free_all = crud.free_list(db=db)
    return paginate(free_all)

@router.get("/frees/{free_id}")
def free_detail(free_id:int,db: Session = Depends(get_db)):
    return crud.get_free(db=db, id=free_id)

@router.delete("/frees/{free_id}")
async def delete(free_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, free_id)
    return {"deleted": deleted}

# @router.put("/frees/{free_id}", response_model=schemas.FreeUpdate, status_code=200)
# async def put_free(free_id: int, free: schemas.FreeList,
#     # #file: UploadFile= File(...),
#     db: Session = Depends(get_db)):
#     # extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
#     # if not extension:
#     #     return "Image must be jpg or png format!"
    
#     # # outputImage = Image.fromarray(sr_img)  
#     # suffix = Path(file.filename).suffix
#     # filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
#     # with open("static/"+filename, "wb") as image:
#     #     shutil.copyfileobj(file.file, image)

#     # #url = str("media/"+file.filename)
#     # url = os.path.join(images_path, filename)
#     db_free = schemas.FreeUpdate(db=db, id =free_id, title=free.title, desc=free.desc,name=free.name)

#     return await crud.update_free(db=db, free=db_free) # Added return

# @router.patch("/frees/{free_id}", response_model=schemas.FreeUpdate, status_code=200)
# async def patch_note(free: schemas.FreeUpdate, db: Session = Depends(get_db)):

#     print(free.id)
#     print(free.title)
#     print(free.desc)
#     db_free = schemas.FreeUpdate(id =free.id, title= free.title, desc=free.desc, name= free.name)

#     return crud.update_free(db=db, free=db_free) # Added return
    
# @router.put("/subjects/{subject_id}")
# async def update_subject(
#     #user : schemas.SubjectUpdate,
#     subject_id: int,
#     title:str,desc:str,name:str,file: UploadFile= File(...), db: Session = Depends(get_db)
# ):
#     extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
#     if not extension:
#         return "Image must be jpg or png format!"
    
#     # outputImage = Image.fromarray(sr_img)  
#     suffix = Path(file.filename).suffix
#     filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
#     with open("static/"+filename, "wb") as image:
#         shutil.copyfileobj(file.file, image)

#     #url = str("media/"+file.filename)
#     url = os.path.join(images_path, filename)
#     subject =  crud.get_subject(db,subject_id)
#     if not subject:
#         raise HTTPException(status_code=404, detail="comment not found")

#     return await crud.update_subject(db=db,subject_id=subject_id,name=name,title=title,desc=desc,url=url)
#     #return {"updated" : updated}


# @router.put("/subjects/{id}/", response_model=SubjectBase)
# async def update_subject(payload: SubjectUpdate,db: Session = Depends(get_db)):
#     subject = await crud.get_subject(db,id)
#     if not subject:
#         raise HTTPException(status_code=404, detail="comment not found")

#     subject_id = await crud.put(id, payload)

#     response_object ={
#         "id": subject_id,
#         "Name": payload.name,
#         "title": payload.title,
#         "description": payload.desc,
#    }
#     return response_object(**Dict)

# @router.put("/subjects/{id}",response_model=SubjectList)
# async def update_subject(subject : SubjectUpdate, db: Session = Depends(get_db)):
    
#     update = await crud.put_sub(db, subject, models.Subject.id)

#     return {"update" : update}
#     #return await find_user_by_id(user.id)

from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session
from . import crud, models
#from courses_live.database import SessionCourse, some_engine
from writer.database import SessionLocal, engine
import shutil
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

@router.post("/filmo/")
def create_filmo(
    title:str,desc:str,status:int,file: UploadFile= File(...), db: Session = Depends(get_db)
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
    return crud.create_filmo(db=db,status=status,title=title,desc=desc,url=url)

@router.get("/filmos/" ,dependencies=[Depends(pagination_params)])
def filmo_list(db: Session = Depends(get_db)):
    filmo_all = crud.filmo_list(db=db)
    return paginate(filmo_all)

@router.get("/filmos/{filmo_id}")
def filmo_detail(filmo_id:int,db: Session = Depends(get_db)):
    return crud.get_filmo(db=db, id=filmo_id)

@router.delete("/filmos/{filmo_id}")
async def delete(filmos_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, filmos_id)
    return {"deleted": deleted}
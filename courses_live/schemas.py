from typing import Optional
from pydantic import BaseModel
import datetime
class LiveBase(BaseModel):
    title:str
    name :str
    desc:str
    
class LiveList(LiveBase):
    created_date: Optional[datetime.datetime]
   
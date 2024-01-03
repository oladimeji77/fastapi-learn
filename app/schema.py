from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from pydantic.types import conint
from pydantic import ConfigDict

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #created_at: Optional[datetime] this is created by the db
    

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True 

class PostResponse(PostBase):
    owner_id: int
    created_at: datetime
    id: int
    owner: UserOut
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password:str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
class PostVote(PostBase):
    model_config: ConfigDict(from_attributes=True)
    Blog: PostResponse
    votes: int   



        
#Schema: it defines the structure of a request and response
# you can create as many pydantic models/schema here and call it in the main.py
# using schema.class eg schema.Blog or schema.PostCreate as the response type

#you can declare your respose model/schema as well
#this would allow pydantic show you only the response that you want to see
#By default the response model will show you everythig in the models.py
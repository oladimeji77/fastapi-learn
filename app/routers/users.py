
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from database import get_db
import models, schema
from sqlalchemy.orm import Session
from typing import Optional, List
from utils import hash

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    query_user = db.query(models.User).filter(models.User.email == user.email).first()
    if query_user != None:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS, detail=f"the user already exist")
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    query_user = db.query(models.User).filter(models.User.id == id).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exist")
    return query_user

@router.get("/", response_model=List[schema.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    query_user = db.query(models.User).all()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exist")
    return query_user
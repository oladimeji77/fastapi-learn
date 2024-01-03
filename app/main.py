from fastapi import FastAPI, Depends
from routers import post, users, auth, vote
from utils import hash
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from database import engine

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router) 
app.include_router(vote.router) 



@app.get("/")
def test_ost(db: Session = Depends(get_db)):
    post = db.query(models.Blog).all()
    return  post
    




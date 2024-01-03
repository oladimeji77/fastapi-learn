from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from database import get_db
import models, schema, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func




router = APIRouter(prefix="/posts", tags=['Post'])

@router.get("/") #response model has a list method for get all post
def get_all(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    post = db.query(models.Blog).filter(models.Blog.title.contains(search)).limit(limit).offset(skip).all()   #this would require List in the res model
    # post = db.query(models.Blog).filter(models.Blog.owner_id == current_user.id).all() 
    result = db.query(models.Blog, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Blog.id,
                                        isouter=True).group_by(models.Blog.id)
    result1 = db.query(models.Blog).all()
    print(result)
    return post



@router.get("/{id}", response_model=schema.PostResponse) 
def get_specific(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Blog).filter(models.Blog.id == id)
    filtered_post = post.first()
    print(filtered_post)
    if filtered_post == None:
        raise HTTPException(detail=f"Post with id {id} not found", status_code=status.HTTP_404_NOT_FOUND)
    # if filtered_post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not your post")
    return filtered_post

    
@router.post("/", response_model=schema.PostResponse)
def push_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Blog(owner_id = current_user.id, **post.dict())
    if new_post == None:
        raise HTTPException(detail=f"Post with id: {id} not found", status_code=status.HTTP_404_NOT_FOUND)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", response_model=schema.PostResponse)
def del_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Blog).filter(models.Blog.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not your post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
        
   
@router.put("/{id}", response_model=schema.PostResponse)
def update_post(id: int, blog: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    up_query = db.query(models.Blog).filter(models.Blog.id == id)
    post = up_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not your post, you ain't allowed")
    up_query.update(blog.dict(), synchronize_session=False)
    db.commit()
    new_post = up_query.first()
    return new_post
    
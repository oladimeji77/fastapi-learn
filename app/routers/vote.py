from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from database import get_db
import models, schema, oauth2
from sqlalchemy.orm import Session




router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/")
def votes(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Blog).filter(models.Blog.id == vote.post_id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} doesn't exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote == None:
            new_post = models.Vote(user_id = current_user.id, post_id = vote.post_id)
            db.add(new_post)
            db.commit()
            return {"message": "sucessfully casted Vote"}

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vote already exists")        
    else:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "sucessfully deleted vote"}   
            
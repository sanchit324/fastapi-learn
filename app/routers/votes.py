from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas, utils, oauth
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if found_vote:
        if vote.dir == 0:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote deleted successfully"}
        elif vote.dir == 1: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} already voted on post {vote.post_id}")
    
    else:
        if vote.dir == 1:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "Vote added successfully"}
        elif vote.dir == 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The post is already deleted")
    
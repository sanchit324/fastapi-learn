from .. import models, schemas, utils, oauth
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix="/posts", 
    tags=["Posts"]
)

### PATH OPERATIONS FOR POSTS ###

# Get all Posts
@router.get("/", response_model=List[schemas.PostOutVote])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # Build query with search in both title and content
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)\
        .filter(models.Post.owner_id == current_user.id)\
        .filter(
            or_(
                models.Post.title.contains(search),
                models.Post.content.contains(search)
            )
        )\
        .limit(limit)\
        .offset(skip)\
        .all()
    return results  
  
# Create a new Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    # cursor.execute("""
    #             INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
    #                """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single Post by ID
@router.get("/{id}", response_model=schemas.PostOutVote)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    # cursor.execute("""
    #                SELECT * FROM posts WHERE id = %s
    #                """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.Post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return post
    
# Delete a Post by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    # cursor.execute("""
    #             DELETE FROM posts WHERE id = %s RETURNING *
    #                """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
        
    post.delete(synchronize_session=False)
    db.commit()
    # No return statement needed for 204 No Content response
  
# Update a Post by ID  
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    # cursor.execute("""
    #                UPDATE posts
    #                SET title = %s, content = %s, published = %s 
    #                WHERE id = %s 
    #                RETURNING *
    #                """, (updated_post.title, updated_post.content, updated_post.published, str(id)))
    # updated_post_data = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

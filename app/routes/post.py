from turtle import right
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    posts = db.query(models.Post).all()

    #Query para trazer apenas os posts do usuario logado
    # posts = db.query(models.Post).filter(models.Post.owner_id == user_id).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
                models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post_id(id: int, response: Response, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # detail = db.query(models.Post).filter(models.Post.id == id).first()

    detail = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return detail


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")

    query.delete(synchronize_session=False)
    db.commit()

    return {"message": "post was succesfully deleted"}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_update = post_query.first()

    if post_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if post_update.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_update
from operator import mod
import psycopg2
from psycopg2.extras import RealDictRow
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
import sqlalchemy

from app import oauth2
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.PostOut])
# @router.get('/', )
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str]= ''):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user), ):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute('INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *', (post.title, post.content, post.publish))
    # # cursor.execute('SELECT LASTVAL()')
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post


@router.get('/{id}', response_model=schemas.PostOut)
async def get_single_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # cursor.execute('SELECT * FROM posts WHERE %s = id', (id,))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute('DELETE FROM posts WHERE %s = id RETURNING *', (id,))
    # if not cursor.fetchone():
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} does not exist')
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized for this action')
    # conn.commit()
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()
    # cursor.execute('UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *',
    #                 (post.title, post.content, post.publish, id))
    # updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} does not exist')
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized for this action')
    # conn.commit()
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    return query.first()
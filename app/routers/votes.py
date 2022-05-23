from operator import mod
from statistics import mode
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/votes',
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {vote.post_id} does not exist')
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully upvoted'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'successfully downvoted'}

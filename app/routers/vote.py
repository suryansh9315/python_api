from fastapi import status, HTTPException, APIRouter, Depends
from .. import schemas, database, utils

router = APIRouter(prefix='', tags=['vote'])
conn, cursor = database.get_db()

@router.post('/vote', status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, user: dict = Depends(utils.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (vote.post_id,))
    current_post = cursor.fetchone()
    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post does not exist")
    cursor.execute("""SELECT * FROM votes WHERE post_id = %s AND voter_id = %s""", (vote.post_id,user['id']))
    current_vote = cursor.fetchone()
    if(vote.dir == 1):
        if current_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User already voted on the post")
        cursor.execute("""INSERT INTO votes (post_id, voter_id) VALUES (%s, %s) RETURNING *""", (vote.post_id, user['id']))
        cursor.fetchone()
        conn.commit()
        return {"message": "Successfully added vote"}
    else:
        if not current_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        cursor.execute("""DELETE FROM votes WHERE post_id = %s AND voter_id = %s RETURNING *""", (vote.post_id, user['id']))
        cursor.fetchone()
        conn.commit()
        return {"message": "Successfully deleted vote"}

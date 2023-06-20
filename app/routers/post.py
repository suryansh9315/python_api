from fastapi import status, HTTPException, APIRouter, Depends
from .. import schemas, database, utils
from typing import List, Optional

router = APIRouter(prefix='', tags=['posts'])
conn, cursor = database.get_db()

@router.get("/posts", response_model=List[schemas.AllPostRes])
async def get_all_posts(limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    search = '%' + search.lower() +'%'
    cursor.execute("""SELECT title, content, email, user_id, posts.id FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE title LIKE %s LIMIT %s OFFSET %s""", (search, limit, skip,))
    posts = cursor.fetchall()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRes)
async def create_post(post: schemas.Post, user: int = Depends(utils.get_current_user)):
    cursor.execute("""INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, user['id']))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post

@router.get("/posts/{id}", response_model=schemas.AllPostRes)
async def get_post_by_id(id: int):
    cursor.execute("""SELECT title, content, email, user_id, posts.id FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE posts.id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

@router.delete("/posts/{id}", response_model=schemas.PostRes)
async def delete_post(id: int, user: int = Depends(utils.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    current_post = cursor.fetchone()
    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if current_post['user_id'] != user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    return deleted_post

@router.put("/posts/{id}", response_model=schemas.PostRes)
async def update_post(id: int, post: schemas.Post, user: int = Depends(utils.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    current_post = cursor.fetchone()
    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if current_post['user_id'] != user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized")
    cursor.execute("""UPDATE posts SET title = %s, content = %s, user_id = %s WHERE id = %s RETURNING *""", (post.title, post.content, user['id'], str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    return updated_post


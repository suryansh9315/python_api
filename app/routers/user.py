from fastapi import status, HTTPException, APIRouter, Depends
from .. import schemas, database, utils

router = APIRouter(prefix='', tags=['users'])
conn, cursor = database.get_db()

@router.post("/login", response_model=schemas.Token)
async def login_user(user_credentials: schemas.Login):
    cursor.execute("""SELECT * FROM users WHERE email = %s""", (user_credentials.email,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = utils.create_access_token(data= {"user_id": user['id']})
    return {'access_token': access_token, "token_type": "bearer"}

# @router.get("/user",response_model=schemas.UserRes)
# async def get_user(user: int = Depends(utils.get_current_user)):
#     return user

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
async def create_user(user: schemas.UserCreate):
    cursor.execute("""SELECT * FROM users WHERE email = %s""",(user.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= f"user with email:{user.email} already exists")
    hashed_password = utils.hash(user.password)
    cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *""", (user.email, hashed_password))
    new_user = cursor.fetchone()
    conn.commit()
    return new_user



from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from random import randrange
from . import database
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
conn, cursor = database.get_db()

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({'exp': expire})
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('user_id')
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},)
    user_id = verify_access_token(token, credentials_exception)
    cursor.execute("""SELECT * FROM users WHERE id = %s""", (str(user_id),))
    user = cursor.fetchone()
    if not user:
        raise credentials_exception
    return user

def generate_random_id(check_db: str):
    temp_id = randrange(0,1000000000)
    if check_db == 'users_id':
        cursor.execute("""SELECT * FROM users_id WHERE id = %s""", (str(temp_id),))
    else:
        cursor.execute("""SELECT * FROM posts_id WHERE id = %s""", (str(temp_id),))
    user = cursor.fetchone()
    if user:
        temp_id = generate_random_id(check_db)
    return temp_id
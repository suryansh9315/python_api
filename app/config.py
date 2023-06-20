from pydantic import BaseSettings

class Settings(BaseSettings):
    database_name: str 
    database_hostname: str
    database_username: str
    database_password: str
    database_port: str
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'

settings = Settings()
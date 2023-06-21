from fastapi import FastAPI
from .routers import post, user, vote
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello Boyaa"}


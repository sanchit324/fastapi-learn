from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Application",
    description="A FastAPI application with user authentication and posts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(votes.router)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the FastAPI Application!",
        "documentation": "/docs",
        "redoc": "/redoc"
    }
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import UserLogin
from .. import models, schemas, utils, oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    password_check: bool = utils.verify(user_credentials.password, user.password)
    
    if not password_check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
        
    # Create a JWT token and return 
    encoded_token = oauth.create_access_token(data={"user_id": user.id})
    
    return {
        "access_token": encoded_token,
        "token_type": "bearer"
    }

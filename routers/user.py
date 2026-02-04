from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from routers import auth
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User as users
from starlette import status

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependancy = Annotated[dict, Depends(auth.get_currentuser)]  
db_dependancy = Annotated[Session, Depends(get_db)]

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user(user: Annotated[dict, Depends(auth.get_currentuser)], db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(users).filter(users.id == user.get("id")).first()
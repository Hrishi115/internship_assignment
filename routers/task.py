from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel
from routers import auth
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task
from starlette import status

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateTaskRequestModel(BaseModel):
    task_title: str
    task_description: str

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(auth.get_currentuser)]

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(TaskModel: CreateTaskRequestModel, user: user_dependancy, db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    new_task = Task(
        task_title=TaskModel.task_title,
        task_description=TaskModel.task_description,
        owner_id=user.get("id"),
        status=False
    )

    db.add(new_task)
    db.commit()
    return {"detail": "Task created successfully"}

@router.get("/get_all_my_tasks", status_code=status.HTTP_200_OK)
async def get_all_my_tasks(user: user_dependancy, db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    return db.query(Task).filter(Task.owner_id == user.get("id")).all()

@router.get("/get_task/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(user: user_dependancy, db: db_dependancy, task_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    task = db.query(Task).filter(Task.task_id == task_id, Task.owner_id == user.get("id")).first()
    return task


@router.put("/update_status/{task_id}", status_code=status.HTTP_200_OK)
async def update_task_status(user: user_dependancy, db: db_dependancy, task_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    task = db.query(Task).filter(Task.task_id == task_id, Task.owner_id == user.get("id")).first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")
    
    db.query(Task).filter(Task.task_id == task_id).update({"status": True})
    db.commit()
    return {"detail": "Task updated successfully"}

@router.delete("/delete/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: int, user: user_dependancy, db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    task = db.query(Task).filter(Task.task_id == task_id, Task.owner_id == user.get("id")).first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")
    
    db.query(Task).filter(Task.task_id == task_id, Task.owner_id == user.get("id")).delete()
    db.commit()
    return {"detail": "Task deleted successfully"}
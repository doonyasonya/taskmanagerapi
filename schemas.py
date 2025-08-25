from pydantic import BaseModel
from typing import Optional
import uuid
from models import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class Task(TaskBase):
    id: uuid.UUID
    status: TaskStatus

    class Config:
        orm_mode = True

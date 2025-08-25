import uuid
from sqlalchemy import Column, String, Enum
from database import Base
import enum


class TaskStatus(str, enum.Enum):
    created = "created"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.created)

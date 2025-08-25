from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager")


@app.get("/")
def root():
    return {"message": "Task Manager API работает"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Валидация перехода статусов ---
def validate_status_transition(
        old_status: models.TaskStatus,
        new_status: models.TaskStatus
):
    allowed = {
        models.TaskStatus.created: [models.TaskStatus.in_progress],
        models.TaskStatus.in_progress: [models.TaskStatus.done],
        models.TaskStatus.done: []  # из "done" больше нельзя никуда
    }
    if new_status != old_status and new_status not in allowed[old_status]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition: {old_status} → {new_status}"
        )


@app.post(
        "/tasks/",
        response_model=schemas.Task,
        status_code=status.HTTP_201_CREATED
)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks/", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: str,
    update: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = update.dict(exclude_unset=True)

    if "status" in update_data:
        validate_status_transition(task.status, update_data["status"])

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return

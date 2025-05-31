from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
from typing import List
import uuid

from database import database, metadata, engine
from models import tasks

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[""], #http://localhost:5500
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskIn(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class Task(TaskIn):
    id: str

@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(engine)  # ساخت جداول اگر وجود نداشتن

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskIn):
    task_id = str(uuid.uuid4())
    query = tasks.insert().values(id=task_id, **task.dict())
    await database.execute(query)
    return {**task.dict(), "id": task_id}

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    query = tasks.select().where(tasks.c.id == task_id)
    task = await database.fetch_one(query)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, updated_task: TaskIn):
    query = tasks.update().where(tasks.c.id == task_id).values(**updated_task.dict())
    await database.execute(query)
    query2 = tasks.select().where(tasks.c.id == task_id)
    task = await database.fetch_one(query2)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    query = tasks.delete().where(tasks.c.id == task_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
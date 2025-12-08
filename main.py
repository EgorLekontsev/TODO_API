from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import SessionLocal, init_db
import crud

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()


# --- Pydantic схемы ---
class TodoCreate(BaseModel):
    title: str


class TodoRead(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True


# --- Зависимость для сессии БД ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/todos", response_model=list[TodoRead])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@app.post("/todos", response_model=TodoRead)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo.title)


@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, completed: bool, db: Session = Depends(get_db)):
    todo = crud.update_todo_completed(db, todo_id, completed)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Deleted"}

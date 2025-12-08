from sqlalchemy.orm import Session
from db import Todo

def get_todos(db: Session):
    return db.query(Todo).all()

def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, title: str):
    todo = Todo(title=title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def update_todo_completed(db: Session, todo_id: int, completed: bool):
    todo = get_todo(db, todo_id)
    if todo:
        todo.completed = completed
        db.commit()
        db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = get_todo(db, todo_id)
    if todo:
        db.delete(todo)
        db.commit()
    return todo

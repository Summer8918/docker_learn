from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

'''
Browsers enforce the Same-Origin Policy, which prevents web pages from making requests to a 
different domain (or even a different port) than the one that served the page.
CORS is a way for the server to tell the browser: “it’s okay for this origin to call my API.”

By adding CORSMiddleware, you’re telling FastAPI to include special HTTP headers 
(Access-Control-Allow-*) in responses so that browsers will allow frontend code running on 
another origin (like http://localhost:3000) to interact with your backend.
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:81"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoItem(BaseModel):
    id: int
    content: str

class TodoItemCreate(BaseModel):
    content: str

todos: list[TodoItem] = []
id_counter = 1

@app.post("/todos", response_model=TodoItem)
async def create_todo(item: TodoItemCreate):
    global id_counter
    new_todo = TodoItem(id=id_counter, content=item.content)
    todos.append(new_todo)
    id_counter += 1
    return new_todo

@app.get("/todos", response_model=list[TodoItem])
async def read_todos():
    return todos

@app.delete("/todos/{todo_id}")
async def delete_todos(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")


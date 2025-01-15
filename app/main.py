from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pymongo import MongoClient
from .models import Note
import os

app = FastAPI()

# MongoDB 连接
client = MongoClient("mongodb://localhost:27017/")
db = client.whiteboard
notes_collection = db.notes

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_notes(request: Request):
    notes = list(notes_collection.find({}))
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

@app.post("/add_note", response_class=RedirectResponse)
async def add_note(
    request: Request, 
    username: str = Form(...), 
    content: str = Form(...)):
    note = Note(username=username, content=content)
    notes_collection.insert_one(note.dict())
    return RedirectResponse(url="/", status_code=303)

from pydantic import BaseModel

class Note(BaseModel):
    username: str
    content: str

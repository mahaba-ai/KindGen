from pydantic import BaseModel
from typing import List


class ChatEntry(BaseModel):
    role: str
    text: str


class ChatHistory(BaseModel):
    entries: List[ChatEntry]

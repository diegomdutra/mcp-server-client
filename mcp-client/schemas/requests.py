from pydantic import BaseModel


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict = {}


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

from pydantic import BaseModel

class CodeRequest(BaseModel):
    language: str
    code: str

class SuggestionResponse(BaseModel):
    suggestions: list[str]

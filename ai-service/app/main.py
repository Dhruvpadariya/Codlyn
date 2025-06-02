from fastapi import FastAPI
from app.schemas import CodeRequest, SuggestionResponse
from app.services import analyze_code

app = FastAPI()

@app.post("/analyze", response_model=SuggestionResponse)
async def analyze(request: CodeRequest):
    suggestions = analyze_code(request.language, request.code)
    return SuggestionResponse(suggestions=suggestions)
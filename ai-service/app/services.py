import requests
from .config import GROQ_API_KEY  # Use a new var name so you don't confuse it with OpenAI

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"  # or "llama3-8b-8192" if you want lighter

def analyze_code(language: str, code: str):
    prompt = f"Analyze the following {language} code and provide improvement suggestions:\n```{language}\n{code}\n```"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that reviews code."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error if the request failed

    content = response.json()["choices"][0]["message"]["content"]
    suggestions = content.strip().split("\n")
    return suggestions

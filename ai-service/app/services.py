import requests
import logging
from .config import GROQ_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

PROMPT_TEMPLATE = """
You are an expert code reviewer. Analyze the following {language} code and return a list of specific improvements, best practices, or bug fixes.

Code:
```{language}
{code}
"""

def analyze_code(language: str, code: str) -> list[str]:
    prompt = PROMPT_TEMPLATE.format(language=language, code=code)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama3-70b-8192",  # Confirm Groq supports this model
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.2,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        if "choices" in response_data and response_data["choices"]:
            content = response_data["choices"][0]["message"]["content"]
            return content.strip().split("\n")
        else:
            logger.warning("No choices returned in the response.")
            return ["No suggestions returned by the model."]

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return [f"HTTP error: {http_err}"]

    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        return [f"Request error: {req_err}"]

    except Exception as err:
        logger.exception("Unexpected error occurred:")
        return [f"Unexpected error: {err}"]
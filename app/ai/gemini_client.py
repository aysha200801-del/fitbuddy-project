from google import genai
from google.genai import types
from ..config import GEMINI_API_KEY

def generate_text(prompt: str, model: str) -> str:
    if not GEMINI_API_KEY:
        return "DEMO MODE\n\nNo GEMINI_API_KEY is configured. Add it to .env for live Gemini responses.\n\nPrompt received:\n" + prompt[:1000]
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=model, contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=5000)
    )
    text = getattr(response, "text", None)
    if not text: raise RuntimeError("Gemini returned an empty response.")
    return text.strip()

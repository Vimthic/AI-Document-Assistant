import os
from dotenv import load_dotenv
from google import genai
import time
from google.genai.errors import APIError

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
'''
def ask_gemini(prompt):
    # CHANGED: Updated from gemini-2.5-flash to gemini-3.5-flash
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )
    return response.text
'''
def ask_gemini(prompt: str) -> str:
    # Use valid current generation models for fallback
    models_to_try = ["gemini-3.5-flash", "gemini-3.1-flash-lite"]
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
        except APIError as e:
            # Handle server capacity limit (503) or rate limits (429)
            if e.code in [429, 503]:
                print(f"⚠️ {model_name} is temporarily busy ({e.code}). Switching fallback model...")
                time.sleep(1.5)
                continue
            # Raise other structural issues (like auth errors) instantly
            raise e
            
    raise RuntimeError("All configured Gemini endpoints are currently facing high demand. Please retry in a few moments.")

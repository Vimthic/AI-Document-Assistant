import os
from dotenv import load_dotenv
from google import genai
import time
from google.genai.errors import APIError
from typing import Generator
# Import the security-focused log utility
from app.logger import log_api_call

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_gemini(prompt: str) -> Generator[str, None, None]:
    """
    Sends a prompt to Gemini and yields chunks of the response text in real-time.
    Returns a Generator so Streamlit can render it using st.write_stream.
    """
    models_to_try = ["gemini-3.5-flash", "gemini-3.1-flash-lite"]
    
    for model_name in models_to_try:
        try:
            # Safe Logging: Logs API metadata (model & text size) instead of raw text content
            log_api_call(model_name, len(prompt))

            # Streams content piece-by-piece from Gemini
            response_stream = client.models.generate_content_stream(
                model=model_name,
                contents=prompt,
            )
            
            # Yield text chunks piece-by-piece as they arrive from the API
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
            return # Exit successfully once the stream completes
            
        except APIError as e:
            # Handle server capacity limit (503) or rate limits (429)
            if e.code in[429, 503]:
                print(f"⚠️ {model_name} is temporarily busy ({e.code}). Switching fallback model...")
                time.sleep(1.5)
                continue
            # Raise other structural issues (like auth errors) instantly
            raise e
            
    raise RuntimeError("All configured Gemini endpoints are currently facing high demand. Please retry in a few moments.")

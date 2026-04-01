from google import genai
from core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_answer(query: str, context: list):
    prompt = f"""
You are a helpful assistant.
Answer ONLY from the context below.

Context:
{context}

Question:
{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
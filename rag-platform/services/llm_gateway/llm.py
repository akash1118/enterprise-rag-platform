from google import genai
from core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_answer(query: str, context: list):
    prompt = f"""
Answer ONLY using the context below.

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
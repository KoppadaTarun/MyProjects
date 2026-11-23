
from google import genai
import os
from app.generation.prompt_builder import build_prompt

from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)




def generate_answer(question: str, context: str) -> str:

    prompt = build_prompt(question, context)

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
        store=False
    )

    response_text = interaction.output_text

    if not response_text:
        raise ValueError("Gemini returned an empty response")

    return response_text

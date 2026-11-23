from google import genai
from dotenv import load_dotenv

load_dotenv()

# Automatically picks up GEMINI_API_KEY from your environment
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explain how AI works in two sentences.",
)

print(response.text)

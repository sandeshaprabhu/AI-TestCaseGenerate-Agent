import os
from dotenv import load_dotenv
from google import genai

# 1. Load your .env file
load_dotenv()

# 2. Initialize the Google GenAI Client
# It will automatically look for the GEMINI_API_KEY or GOOGLE_API_KEY env var
client = genai.Client()

print("Available models that support text generation:\n")

# 3. List models and filter for those that support 'generateContent'
for m in client.models.list():
    if 'generateContent' in m.supported_actions:
        print(f"- Name: {m.name}")
        print(f"  Display Name: {m.display_name}")
        print(f"  Description: {m.description}\n")

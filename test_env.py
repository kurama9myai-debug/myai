from dotenv import load_dotenv
import os

load_dotenv()

print("کلید API شما:", os.getenv("OPENAI_API_KEY"))

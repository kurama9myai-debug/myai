from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "سلام"}]
    )
    print("✅ اتصال برقرار شد!")
    print("پاسخ:", response.choices[0].message.content)
except Exception as e:
    print("❌ خطا:", e)

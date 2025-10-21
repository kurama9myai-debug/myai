from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
import openai

# کلید API خودت رو اینجا بذار
openai.api_key = "YOUR_API_KEY"

while True:
    user_input = input("شما: ")

    if user_input.lower() in ["exit", "quit", "خروج"]:
        print("ربات: خداحافظ! 🖐️")
        break

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "تو یک دستیار هوش مصنوعی فارسی هستی."},
            {"role": "user", "content": user_input},
        ]
    )
import openai

# 🧠 جایگزین کن با کلید API واقعی خودت
openai.api_key = "YOUR_API_KEY_HERE"

def chat_with_ai():
    print("🤖 سلام! من هوش مصنوعی تو هستم. هر چی خواستی بپرس! (برای خروج بنویس exit)")

    while True:
        user_input = input("👤 تو: ")

        if user_input.lower() == "exit":
            print("خداحافظ دوست من 👋")
            break

        # درخواست به OpenAI برای پاسخ
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        print("🤖 ربات:", response["choices"][0]["message"]["content"])

if name == "main":
    chat_with_ai()
    import openai
import pyttsx3
import speech_recognition as sr
from googletrans import Translator

openai.api_key = "اینجا کلید API خودت رو بزار"

def chat_with_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("در حال گوش دادن...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="fa-IR")
        print("شما گفتید:", text)
        return text
    except:
        return "صدا شنیده نشد"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    print("هوش مصنوعی آماده است! با او صحبت کن (برای خروج بنویس 'خروج')")
    while True:
        import streamlit as st
user_input = st.text_input("شما:")

        if user_input.lower() == "خروج":
            break
        response = chat_with_ai(user_input)
        print("هوش مصنوعی:", response)
        speak(response)

if name == "main":
    main()
    openai.api_key = "import openai"

openai.api_key = "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"

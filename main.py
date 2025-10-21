import streamlit as st
import openai
import os
from dotenv import load_dotenv

# بارگذاری کلید API از .env (اگر داری)
load_dotenv()

# کلید API
openai.api_key = os.getenv("OPENAI_API_KEY") or "sk-proj-...اینجا کلید خودت..."

st.title("🤖 چت‌بات هوش مصنوعی فارسی")

# ذخیره پیام‌ها برای نمایش بهتر
if "messages" not in st.session_state:
    st.session_state.messages = []

# ورودی کاربر
user_input = st.text_input("شما:", "")

if st.button("ارسال") and user_input:
    # پیام کاربر رو ذخیره کن
    st.session_state.messages.append({"role": "user", "content": user_input})

    # پاسخ هوش مصنوعی بگیر
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    ai_reply = response["choices"][0]["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# نمایش چت
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"👤 **شما:** {msg['content']}")
    else:
        st.markdown(f"🤖 **هوش مصنوعی:** {msg['content']}")

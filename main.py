# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# بارگذاری توکن از .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("❌ توکن Hugging Face پیدا نشد. لطفاً در فایل .env مقدار HF_TOKEN را تنظیم کن.")
    st.stop()

# ساخت کلاینت Hugging Face
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

st.title("🤖 چت‌بات فارسی با Llama 3 (Hugging Face)")

# ذخیره پیام‌ها
if "messages" not in st.session_state:
    st.session_state.messages = []

# ورودی کاربر
user_input = st.text_input("شما:", "")

if st.button("ارسال") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=st.session_state.messages
        )
        ai_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    except Exception as e:
        st.error(f"❌ خطا در اتصال: {e}")

# نمایش گفتگو
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"👤 **شما:** {msg['content']}")
    else:
        st.markdown(f"🤖 **هوش مصنوعی:** {msg['content']}")

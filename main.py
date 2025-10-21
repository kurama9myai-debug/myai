# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or "sk-proj-...اینجا کلید خودت..."
client = OpenAI(api_key=api_key)

st.title("🤖 چت‌بات هوش مصنوعی فارسی")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("شما:", "")

if st.button("ارسال") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    ai_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"👤 **شما:** {msg['content']}")
    else:
        st.markdown(f"🤖 **هوش مصنوعی:** {msg['content']}")

# -*- coding: utf-8 -*-
"""
main.py
Streamlit chatbot (Persian) — compatible with both old and new openai package APIs.
Make sure your OPENAI_API_KEY is set in .env or in Render environment variables.
"""

import os
# Force UTF-8 environment early (before importing httpx/openai)
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("LANG", "en_US.UTF-8")
os.environ.setdefault("LC_ALL", "C.UTF-8")

import sys
try:
    # ensure stdout uses utf-8
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import streamlit as st
from dotenv import load_dotenv
import importlib

# load .env (if present)
load_dotenv()

# get API key from env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # If not set, show a warning in the UI (but continue)
    OPENAI_API_KEY = None

# helper: get a client or module that can create chat completions
def get_openai_handler(api_key):
    """
    Tries to return an object that supports chat completions.
    Prefer new API: from openai import OpenAI (client.chat.completions.create)
    Fallback: the legacy openai module with openai.ChatCompletion.create
    Returns a tuple: (mode, handler)
      mode == "new" -> handler is client (OpenAI instance)
      mode == "old" -> handler is the openai module
      mode == "none" -> handler is None
    """
    try:
        # try new style
        openai_pkg = importlib.import_module("openai")
        # try to import OpenAI class
        OpenAI = getattr(openai_pkg, "OpenAI", None)
        if OpenAI:
            client = OpenAI(api_key=api_key) if api_key else OpenAI()
            return "new", client
        # maybe package exposes OpenAI under openai.OpenAI (older new versions)
    except Exception:
        # ignore — will try fallback
        pass

    try:
        # fallback to legacy API
        legacy = importlib.import_module("openai")
        # ensure we set the api_key if not set inside env
        if api_key:
            setattr(legacy, "api_key", api_key)
        return "old", legacy
    except Exception:
        return "none", None


# single function to get AI reply (handles both APIs and errors)
def get_ai_reply(messages):
    """
    messages: list of dicts like {"role": "user"|"assistant"|"system", "content": "..."}
    returns: (ok, reply_or_error_message)
    """
    mode, handler = get_openai_handler(OPENAI_API_KEY)
    if mode == "none" or handler is None:
        return False, "❌ خطا: کتابخانه‌ی OpenAI در محیط در دسترس نیست."

    try:
        if mode == "new":
            # new API: client.chat.completions.create(...)
            # note: some versions use client.chat.completions.create
            response = handler.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            # response.choices[0].message.content
            content = None
            if hasattr(response, "choices") and len(response.choices) > 0:
                # new object style
                content = response.choices[0].message.content
            else:
                # try dict-like
                content = response["choices"][0]["message"]["content"]
            return True, content

        else:
            # old API compatibility
            response = handler.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            # old response style: response["choices"][0]["message"]["content"]
            content = response["choices"][0]["message"]["content"]
            return True, content

    except Exception as e:
        # return exception message (short)
        # avoid exposing long stack traces to user; show helpful hint
        err_text = str(e)
        # common encoding header problem: ensure hint about encoding
        if "latin-1" in err_text or "ascii" in err_text or "UnicodeEncodeError" in err_text:
            hint = (
                "خطای رمزگذاری (encoding) رخ داده — سرور تلاش می‌کند متن فارسی را به فرمت ASCII/Latin-1 بفرستد. "
                "لطفاً مطمئن شو که در Render یا محیط اجرای سرور متغیرهای محیطی `LANG` و `PYTHONIOENCODING` روی UTF-8 تنظیم شده‌اند."
            )
            return False, f"❌ خطای کتابخانه/رمزگذاری: {err_text}\n\n{hint}"
        return False, f"❌ خطای اتصال به OpenAI: {err_text}"


# --- Streamlit UI ---
st.set_page_config(page_title="چت‌بات فارسی", layout="centered")
st.title("🤖 چت‌بات هوش مصنوعی فارسی")

# show small notice if API key not set
if not OPENAI_API_KEY:
    st.warning("کلید OpenAI پیدا نشد. اگر می‌خواهی با OpenAI کار کنی، متغیر محیطی OPENAI_API_KEY را تنظیم کن.")

# maintain conversation in session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "status" not in st.session_state:
    st.session_state.status = ""

# input area
col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input("شما:", value="", key="user_input")
with col2:
    send = st.button("ارسال")

# clear chat button
if st.button("پاک کردن چت"):
    st.session_state.messages = []
    st.experimental_rerun()

# when user sends
if send and user_input:
    # append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # show a temporary status
    st.session_state.status = "در حال گرفتن پاسخ از هوش مصنوعی..."
    with st.spinner(st.session_state.status):
        ok, reply = get_ai_reply(st.session_state.messages)
    st.session_state.status = ""

    if ok:
        st.session_state.messages.append({"role": "assistant", "content": reply})
    else:
        # error -> show message
        st.error(reply)

# display chat messages (old to new)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"👤 **شما:** {msg['content']}")
    else:
        st.markdown(f"🤖 **هوش مصنوعی:** {msg['content']}")

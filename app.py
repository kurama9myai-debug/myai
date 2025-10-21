import streamlit as st
import requests

st.set_page_config(page_title="💰 قیمت ارز دیجیتال", page_icon="💵")

st.title("💰 بررسی قیمت لحظه‌ای ارزهای دیجیتال")
st.write("اسم ارز رو وارد کن (مثل: bitcoin یا ethereum):")

coin_name = st.text_input("نام ارز:")

if st.button("دریافت قیمت"):
    if coin_name:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_name}&vs_currencies=usd"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if coin_name in data:
                price = data[coin_name]["usd"]
                st.success(f"💵 قیمت فعلی {coin_name}: {price} دلار")
            else:
                st.error("❌ نام ارز نادرست است.")
        else:
            st.error("⚠️ خطا در ارتباط با سرور!")
    else:
        st.warning("لطفاً نام ارز را وارد کن.")

# app.py
# -*- coding: utf-8 -*-
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ---------- تنظیمات ----------
st.set_page_config(page_title="Hybrid Crypto Assistant", page_icon="🤖", layout="centered")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "").strip()
USE_OPENAI = bool(OPENAI_KEY)

# ---------- توابع ابزار (tool) ----------
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

def fetch_price(coin_id, vs_currency="usd"):
    try:
        url = f"{COINGECKO_BASE}/simple/price"
        params = {"ids": coin_id, "vs_currencies": vs_currency, "include_24hr_change": "true"}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if coin_id in data and vs_currency in data[coin_id]:
            return {"price": data[coin_id][vs_currency], "change24": data[coin_id].get(f"{vs_currency}_24h_change")}
    except Exception as e:
        return {"error": str(e)}
    return None

# نگاشت اسامی فارسی به شناسه‌های coingecko
MAPPING = {
    "بیتکوین": "bitcoin",
    "بیت‌کوین": "bitcoin",
    "اتریوم": "ethereum",
    "سولانا": "solana",
    "دوج": "dogecoin",
    "دوج‌کوین": "dogecoin",
    # اضافه کن هر کلمه‌ای که می‌خوای
}

def normalize_query(q):
    q = q.strip()
    if not q:
        return ""
    # اگر فارسی وارد شده، تبدیل به شناسه انگلیسی
    if q in MAPPING:
        return MAPPING[q]
    # معمولاً کاربر انگلیسی مینویسه مثل "bitcoin"
    return q.lower()

# ---------- پاسخ محلی (fallback) ----------
def local_response(user_text):
    u = user_text.strip().lower()
    # دستور گرفتن قیمت: "قیمت bitcoin" یا فقط "bitcoin"
    if u.startswith("قیمت "):
        coin = u.replace("قیمت ", "").strip()
        coin = normalize_query(coin)
        res = fetch_price(coin)
        if isinstance(res, dict) and "price" in res:
            return f"💰 قیمت فعلی {coin}: {res['price']} USD (24h change: {res.get('change24')})"
        else:
            return f"❌ خطا یا ارز پیدا نشد: {res}"
    # اگر کاربر فقط نام ارز را نوشت
    if u in MAPPING or len(u) <= 20 and all(c.isalpha() or c in ("-", "_", " ") for c in u):
        coin = normalize_query(u)
        res = fetch_price(coin)
        if isinstance(res, dict) and "price" in res:
            return f"💰 قیمت فعلی {coin}: {res['price']} USD (24h change: {res.get('change24')})"
        else:
            return "❌ ارز پیدا نشد یا خطای شبکه."
    # سوالات ساده‌ای مثل "سلام" یا "حالت چطوره"
    if u in ("سلام", "سلام!","سلامی"):
        return "سلام! من دستیار ترید تو هستم — اسم یک ارز را بگو یا 'قیمت bitcoin' بنویس."
    if any(w in u for w in ("چطوری", "چطوری؟", "چطوری هستی")):
        return "خوبم ممنون، آماده‌ام در مورد قیمت‌ها یا تحلیل ساده کمک کنم."
    # fallback کلی
    return None  # به معنی این‌که هیچ پاسخ محلی نداریم

# ---------- تابع تماس به OpenAI (اختیاری و امن) ----------
def openai_response(user_text):
    # فقط وقتی کلید موجود است، این تابع استفاده شود
    try:
        if not USE_OPENAI:
            return None
        import openai
        openai.api_key = OPENAI_KEY
        # درخواست ساده chat completion
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system", "content":"تو یک دستیار تولید پاسخ فارسی و کمک به تحلیل قیمت رمزارزها هستی."},
                {"role":"user", "content": user_text}
            ],
            max_tokens=512,
            temperature=0.2,
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenAI error] {e}"

# ---------- UI و حلقهٔ چت ----------
st.title("🤖 دستیار ترکیبی رمزارز (Hybrid)")
st.markdown("این دستیار می‌تواند قیمت‌ها را از اینترنت بگیرد و برای پرسش‌های آزاد از مدل ابری (OpenAI) استفاده کند *در صورت وجود کلید*.")
if USE_OPENAI:
    st.success("OpenAI فعال است: پاسخ‌های پیچیده‌تر با OpenAI انجام می‌شوند.")
else:
    st.info("OpenAI غیر فعال است — اپ با منطق محلی و ابزارها کار می‌کند.")

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.form("input_form", clear_on_submit=True):
    user_input = st.text_input("پیام شما (فارسی/انگلیسی):")
    submit = st.form_submit_button("ارسال")
if submit and user_input:
    st.session_state.chat.append(("شما", user_input))
    # اول تلاش برای پاسخ محلی
    local = local_response(user_input)
    if local:
        st.session_state.chat.append(("ربات", local))
    else:
        # اگر کلید OpenAI هست، از اون استفاده کن
        if USE_OPENAI:
            st.session_state.chat.append(("ربات", "در حال پرسش از مدل ابری..."))
            reply = openai_response(user_input)
            st.session_state.chat.pop()  # حذف پیام 'در حال پرسش...'
            st.session_state.chat.append(("ربات", reply or "مدل ابری پاسخی نداد."))
        else:
            st.session_state.chat.append(("ربات", "متاسفم — نمی‌تونم به صورت هوشمند جواب بدم. اسم یک ارز یا 'قیمت X' را امتحان کن."))

# نمایش گفتگو (جدیدترین در بالا)
for speaker, text in reversed(st.session_state.chat):
    if speaker == "شما":
        st.markdown(f"**{speaker}:** {text}")
    else:
        st.markdown(f"**{speaker}:** {text}")
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# بررسی وجود کلید
has_openai = bool(api_key and len(api_key) > 10)

# ---- تابع بررسی قیمت رمزارز ----
def get_crypto_price(coin_id="bitcoin"):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        if coin_id in data:
            return data[coin_id]["usd"]
        else:
            return None
    except Exception as e:
        return f"❌ خطا در دریافت داده‌ها: {e}"

# ---- تابع گفت‌وگو با OpenAI ----
def ask_openai(question):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "تو یک دستیار فارسی‌زبان هستی."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ خطا در ارتباط با OpenAI: {e}"

# ---- رابط کاربری Streamlit ----
st.title("💬 دستیار ترکیبی رمزارز (Hybrid AI)")

st.markdown("این برنامه می‌تواند هم به صورت **آفلاین** (برای قیمت رمزارزها) و هم **آنلاین** (با هوش مصنوعی OpenAI) کار کند.")

st.write(f"🔑 وضعیت OpenAI: {'✅ فعال' if has_openai else '❌ غیرفعال'}")

mode = st.radio("حالت مورد نظر را انتخاب کنید:", ["هوش مصنوعی / پرسش آزاد", "قیمت ارز دیجیتال"])

if mode == "قیمت ارز دیجیتال":
    coin = st.text_input("🔹 نام ارز (مثلاً bitcoin یا ethereum):")
    if st.button("نمایش قیمت"):
        price = get_crypto_price(coin.lower())
        if price:
            st.success(f"💰 قیمت فعلی {coin}: {price} دلار")
        else:
            st.error("❌ ارز پیدا نشد یا خطایی رخ داد.")
else:
    question = st.text_area("🧠 پیام خود را بنویس:")
    if st.button("ارسال"):
        if has_openai:
            answer = ask_openai(question)
            st.write("🤖 پاسخ:", answer)
        else:
            st.warning("🔒 برای فعال کردن پاسخ‌های هوشمند باید کلید OpenAI را در فایل .env قرار دهی.")

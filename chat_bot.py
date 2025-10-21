import requests

def get_crypto_price(coin_id="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if coin_id in data:
            price = data[coin_id]["usd"]
            print(f"💰 قیمت فعلی {coin_id}: {price} دلار")
        else:
            print("❌ ارز پیدا نشد. مطمئن شو اسمش درسته.")
    else:
        print("❌ خطا در دریافت داده‌ها:", response.status_code)


# حلقه‌ی چت
if __name__ == "__main__":
    print("سلام! 👋 اسم ارز دیجیتال رو بنویس (مثل bitcoin یا ethereum). برای خروج بنویس exit.")
    while True:
        user_input = input("شما: ").strip().lower()
        if user_input == "exit":
            print("خداحافظ! 👋")
            break
        get_crypto_price(user_input)

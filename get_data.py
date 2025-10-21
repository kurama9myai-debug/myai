import requests

def get_crypto_price(coin_id="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price = data[coin_id]["usd"]
        print(f"💰 قیمت فعلی {coin_id}: {price} دلار")
    else:
        print("❌ خطا در دریافت داده‌ها:", response.status_code)

if __name__ == "__main__":
    get_crypto_price("bitcoin")

import os
import requests
import matplotlib.pyplot as plt
import telebot

GOLDAPI_KEY = os.getenv("GOLDAPI_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HEADERS = {
    "x-access-token": GOLDAPI_KEY,
    "Content-Type": "application/json"
}

# --- 1) Frankfurter API ile USD/EUR fiyatları ---
def get_fx_rate(symbol):
    # Örnek: symbol = "USD", "EUR"
    url = f"https://api.frankfurter.app/latest?from={symbol}&to=TRY"
    r = requests.get(url)
    data = r.json()
    return data["rates"]["TRY"]


# --- 2) GoldAPI ile altın / gümüş gram fiyatı ---
def get_metal_price(symbol):
    url = f"https://www.goldapi.io/api/{symbol}/TRY"
    r = requests.get(url, headers=HEADERS)
    data = r.json()

    if "price_gram_24k" in data:
        return data["price_gram_24k"]
    else:
        print("GoldAPI Hatası:", data)
        return None


def generate_chart(usd, eur, altin, gumus):
    labels = ['USD', 'EUR', 'Altın', 'Gümüş']
    values = [usd, eur, altin, gumus]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values)
    plt.title("Günlük Finans Özeti")
    plt.tight_layout()
    plt.savefig("chart.png")
    plt.close()


def main():
    # Döviz
    usd = get_fx_rate("USD")
    eur = get_fx_rate("EUR")

    # Altın & Gümüş
    altin = get_metal_price("XAU")
    gumus = get_metal_price("XAG")

    # Telegram
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

    text = f"""
📊 Günlük Finans Özeti

💵 USD/TRY: {usd}
💶 EUR/TRY: {eur}
🥇 Gram Altın (XAU): {altin}
🥈 Gram Gümüş (XAG): {gumus}

Grafik hazırlanıyor...
"""

    bot.send_message(TELEGRAM_CHAT_ID, text)

    generate_chart(usd, eur, altin, gumus)

    with open("chart.png", "rb") as img:
        bot.send_photo(TELEGRAM_CHAT_ID, img)


if __name__ == "__main__":
    main()

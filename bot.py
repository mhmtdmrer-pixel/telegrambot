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

def get_price(symbol):
    """USD/TRY, EUR/TRY gibi döviz fiyatını almak için"""
    url = f"https://www.goldapi.io/api/{symbol}/TRY"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    return data["price"]

def get_metal_price(metal):
    """XAU (altın) ve XAG (gümüş) gram fiyatını almak için"""
    url = f"https://www.goldapi.io/api/{metal}/TRY"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    return data["price_gram_24k"]

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
    usd = get_price("USD")
    eur = get_price("EUR")
    altin = get_metal_price("XAU")
    gumus = get_metal_price("XAG")

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

import os
import requests
import matplotlib.pyplot as plt
import telebot

# Fiyatları alma
def get_prices():
    url_xau = "https://www.goldapi.io/api/XAU/TRY"
    url_xag = "https://www.goldapi.io/api/XAG/TRY"

    headers = {
        "x-access-token": os.getenv("GOLDAPI_KEY"),
        "Content-Type": "application/json"
    }

    # Altın
    r1 = requests.get(url_xau, headers=headers)
    r1.raise_for_status()
    data_xau = r1.json()

    # Gümüş
    r2 = requests.get(url_xag, headers=headers)
    r2.raise_for_status()
    data_xag = r2.json()

    usd_try = data_xau["exchange_rate"]["USD"]
    eur_try = data_xau["exchange_rate"]["EUR"]

    gram_altin = data_xau["price_gram_24k"]
    gram_gumus = data_xag["price_gram_24k"]

    return usd_try, eur_try, gram_altin, gram_gumus


# Telegram mesaj gönderme
def send_telegram_message(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    bot = telebot.TeleBot(token)
    bot.send_message(chat_id, text)


# Görsel üretme
def generate_chart(usd, eur, altin, gumus):
    labels = ['USD', 'EUR', 'Altın (24K)', 'Gümüş']
    values = [usd, eur, altin, gumus]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values)
    plt.title("Günlük Fiyat Özeti")
    plt.tight_layout()
    plt.savefig("chart.png")
    plt.close()


# Telegram görsel gönderme
def send_telegram_image():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    bot = telebot.TeleBot(token)
    with open("chart.png", "rb") as img:
        bot.send_photo(chat_id, img)


# Ana
def main():
    usd, eur, altin, gumus = get_prices()

    text = f"""
📊 Günlük Finans Özeti

💵 USD/TRY: {usd}
💶 EUR/TRY: {eur}
🥇 Gram Altın: {altin} TL
🥈 Gram Gümüş: {gumus} TL

Grafik hazırlanıyor ve birazdan gönderiliyor.
"""

    send_telegram_message(text)

    generate_chart(usd, eur, altin, gumus)
    send_telegram_image()


if __name__ == "__main__":
    main()

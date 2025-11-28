import os
import requests
import telebot

# ENV değişkenleri
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# 1) Frankfurter API — USD / EUR
def get_fx_rate(symbol):
    url = f"https://api.frankfurter.app/latest?from={symbol}&to=TRY"
    r = requests.get(url)
    data = r.json()
    return round(data["rates"]["TRY"], 3)

# 2) Genelpara API — Altın & Gümüş
def get_metal_prices():
    url = "https://api.genelpara.com/embed/altin.json"
    r = requests.get(url)
    data = r.json()

    gram_altin = float(data["gram_altin"]["satis"].replace(",", "."))
    gram_gumus = float(data["gumus"]["satis"].replace(",", "."))

    return gram_altin, gram_gumus


def main():
    # Döviz
    usd = get_fx_rate("USD")
    eur = get_fx_rate("EUR")

    # Altın & Gümüş
    altin, gumus = get_metal_prices()

    text = f"""
📊 Günlük Finans Özeti

💵 USD/TRY: {usd}
💶 EUR/TRY: {eur}
🥇 Gram Altın: {altin} TL
🥈 Gram Gümüş: {gumus} TL
"""

    bot.send_message(TELEGRAM_CHAT_ID, text)


if __name__ == "__main__":
    main()

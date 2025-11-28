import os
import requests
import telebot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# TradingView / Binance API fiyat çekici
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    r = requests.get(url)
    data = r.json()
    return float(data["price"])

def main():
    # Döviz
    usd_try = get_price("USDTRY")
    eur_try = get_price("EURTRY")

    # XAUUSD ve XAGUSD dolar fiyatları
    xau_usd = get_price("XAUUSD")
    xag_usd = get_price("XAGUSD")

    # Gram Altın & Gram Gümüş
    gram_altin = (xau_usd / usd_try) / 31.103
    gram_gumus = (xag_usd / usd_try) / 31.103

    # Yuvarlama
    gram_altin = round(gram_altin, 2)
    gram_gumus = round(gram_gumus, 2)
    usd_try = round(usd_try, 3)
    eur_try = round(eur_try, 3)

    text = f"""
📊 Günlük Finans Özeti

💵 USD/TRY: {usd_try}
💶 EUR/TRY: {eur_try}
🥇 Gram Altın: {gram_altin} TL
🥈 Gram Gümüş: {gram_gumus} TL
"""

    bot.send_message(TELEGRAM_CHAT_ID, text)

if __name__ == "__main__":
    main()

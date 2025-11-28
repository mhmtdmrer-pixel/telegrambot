import os
import requests
import telebot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# 1) Frankfurter API — Döviz fiyatları
def get_fx_rate(base, target="TRY"):
    url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
    r = requests.get(url)
    data = r.json()
    return float(data["rates"][target])


# 2) TradingView (Binance proxy) — XAUUSD & XAGUSD
def get_commodity_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    r = requests.get(url)
    data = r.json()

    if "price" not in data:
        raise ValueError(f"API 'price' döndürmedi: {data}")

    return float(data["price"])


def main():
    # Döviz
    usdtry = get_fx_rate("USD")
    eurtry = get_fx_rate("EUR")

    # Ons Altın & Ons Gümüş (USD)
    xauusd = get_commodity_price("XAUUSD")
    xagusd = get_commodity_price("XAGUSD")

    # Gram Altın & Gram Gümüş
    gram_altin = round((xauusd / usdtry) / 31.103, 2)
    gram_gumus = round((xagusd / usdtry) / 31.103, 2)

    # Mesaj metni
    text = f"""
📊 Günlük Finans Özeti

💵 USD/TRY: {round(usdtry, 3)}
💶 EUR/TRY: {round(eurtry, 3)}
🥇 Gram Altın: {gram_altin} TL
🥈 Gram Gümüş: {gram_gumus} TL
"""

    bot.send_message(TELEGRAM_CHAT_ID, text)


if __name__ == "__main__":
    main()

import os
import requests
from bs4 import BeautifulSoup
import telebot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def google_price(query):
    q = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find("span", class_="pclqee")
    if result:
        return float(result.text.replace(",", "."))
    else:
        return None


def main():
    usd = google_price("usd try")
    eur = google_price("eur try")
    altin = google_price("gram altın fiyatı")
    gumus = google_price("gram gümüş fiyatı")

    text = f"""
📊 Günlük Finans Özeti (API YOK — Stabil Sistem)

💵 USD/TRY: {usd}
💶 EUR/TRY: {eur}
🥇 Gram Altın: {altin}
🥈 Gram Gümüş: {gumus}
"""

    bot.send_message(TELEGRAM_CHAT_ID, text)


if __name__ == "__main__":
    main()

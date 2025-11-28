import os
import requests
import telebot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_prices():
    url = "https://finans.truncgil.com/today.json"
    r = requests.get(url)
    data = r.json()

    usd = float(data["USD"]["Satış"].replace(",", "."))
    eur = float(data["EUR"]["Satış"].replace(",", "."))
    altin = float(data["Gram Altın"]["Satış"].replace(",", "."))
    gumus = float(data["Gümüş"]["Satış"].replace(",", "."))

    return usd, eur, altin, gumus


def main():
    usd, eur, altin, gumus = get_prices()

    text = f"""
📊 Günlük Finans Özeti

💵 USD/TRY: {usd}
💶 EUR/TRY: {eur}
🥇 Gram Altın: {altin}
🥈 Gram Gümüş: {gumus}
"""

    bot.send_message(TELEGRAM_CHAT_ID, text)


if __name__ == "__main__":
    main()

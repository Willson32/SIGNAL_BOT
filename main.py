import time
import telegram
from config import BOT_TOKEN, CHAT_ID
from signals import get_signals

bot = telegram.Bot(token=BOT_TOKEN)

def send_signals():
    signals = get_signals()
    if signals:
        message = "📊 *Crypto Signals*\n\n" + "\n".join(signals)
    else:
        message = "⏳ Пока нет чётких сигналов."
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    while True:
        send_signals()
        time.sleep(20 * 60)  # каждые 20 минут
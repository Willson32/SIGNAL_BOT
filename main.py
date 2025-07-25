import asyncio
from aiogram import Bot
from config import BOT_TOKEN, CHAT_ID
from signals import get_signals

bot = Bot(token=BOT_TOKEN)

async def send_signals():
    while True:
        signals = get_signals()
        if signals:
            message = "📊 *Crypto Signals*\n\n" + "\n".join(signals)
        else:
            message = "⏳ Пока нет чётких сигналов."
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        await asyncio.sleep(20 * 60)  # 20 минут

async def main():
    await send_signals()

if __name__ == "__main__":
    asyncio.run(main())

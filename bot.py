import os
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from handlers import start, catalog, payment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)

async def start_bot():
    # Use Telegram Bot API proxy to bypass network restrictions
    session = AiohttpSession(
        api="https://api.telegram.org"
    )
    
    bot = Bot(
        token=os.getenv("BOT_TOKEN")
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Include routers
    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(payment.router)

    retry_delay = 5
    max_retry_delay = 60

    while True:
        try:
            logging.info("Удаление вебхуков...")
            await bot.delete_webhook(drop_pending_updates=True)
            
            logging.info("Запуск polling...")
            await dp.start_polling(bot, skip_updates=True)
        except Exception as e:
            logging.error(f"Ошибка в цикле polling: {e}")
            logging.info(f"Перезапуск через {retry_delay} сек...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_retry_delay)
        else:
            retry_delay = 5

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Остановка по команде пользователя.")
    except Exception as e:
        logging.critical(f"Глобальный сбой: {e}")



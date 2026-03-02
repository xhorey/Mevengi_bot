import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os
from app.handlers.basic_handlers import router
from app.handlers.bank_handlers import router_bank
from app.handlers.casino_handlers import router_casino
from app.handlers.treatment_handlers import router_treatment
from app.handlers.tap_handlers import router_tap
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


dp = Dispatcher()



async def main() -> None:

    dp.include_router(router)
    dp.include_router(router_bank)
    dp.include_router(router_casino)
    dp.include_router(router_treatment)
    dp.include_router(router_tap)

    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

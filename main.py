from loguru import logger
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager

import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger

from app.config import bot, admins, dp, settings
from bot.users.router import user_router
from bot.admin.router import admin_router
from bot.middlewares.is_admin import CheckIsAdmin
from bot.middlewares.anti_floud import AntiFloudMiddleware
from bot.middlewares.white_list import VerificationMiddleware
from aiogram.types import Update
from fastapi import FastAPI, Request
from app.routers.api_router import api_router
app = FastAPI()

# Функция, которая настроит командное меню (дефолтное для всех пользователей)
async def set_commands():
    commands = [BotCommand(command='start', description='Старт')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функция, которая выполнится когда бот запустится
async def start_bot():
    await set_commands()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f'Я запущен🥳.')
        except:
            pass
    logger.info("Бот успешно запущен.")


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass
    logger.error("Бот остановлен!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting bot setup...")
    #регистрация middleware
    admin_router.message.middleware(CheckIsAdmin())
    dp.message.middleware(AntiFloudMiddleware(1))
    dp.message.middleware(VerificationMiddleware())
    #регистрация роутеров
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await start_bot()
    webhook_url = settings.get_webhook_url()
    await bot.set_webhook(url=webhook_url,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    logger.info(f"Webhook set to {webhook_url}")
    yield
    logger.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logger.info("Webhook deleted")

app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logger.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logger.info("Update processed")

app.include_router(api_router)

# async def main():
#     #регистрация middleware
#     admin_router.message.middleware(CheckIsAdmin())
#     dp.message.middleware(AntiFloudMiddleware(1))
#     dp.message.middleware(VerificationMiddleware())
#     # регистрация роутеров
#     dp.include_router(user_router)
#     dp.include_router(admin_router)
    
#     # регистрация функций
#     dp.startup.register(start_bot)
#     dp.shutdown.register(stop_bot)

    
#     try:
#         await bot.delete_webhook(drop_pending_updates=True)
#         await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
#     finally:
#         await bot.session.close()


# if __name__ == "__main__":
#     asyncio.run(main())

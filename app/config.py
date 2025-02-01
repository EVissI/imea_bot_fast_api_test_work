import os
from typing import List
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis.asyncio as aioredis
from contextlib import asynccontextmanager


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    REDIS_IP:str
    REDIS_PORT:str
    REDIS_PASSWORD:str
    BASE_SITE: str
    JWT_SECRET_KEY:str
    JWT_ALGORITM:str
    IMEI_CHECK_TOKEN:str
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    DB_URL: str = 'sqlite+aiosqlite:///data/db.sqlite3'
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )
    def get_webhook_url(self) -> str:
        """Возвращает URL вебхука с кодированием специальных символов."""
        return f"{self.BASE_SITE}/webhook"


# Получаем параметры для загрузки переменных среды
settings = Settings()

# Инициализируем бота и диспетчер
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
redis = aioredis.Redis(
        host=settings.REDIS_IP,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )
dp = Dispatcher(storage=MemoryStorage())
# dp = Dispatcher(storage=RedisStorage(redis))
admins = settings.ADMIN_IDS

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
database_url = settings.DB_URL

@asynccontextmanager
async def redis_session():
    try:
        yield redis
    finally:
        await redis.close()
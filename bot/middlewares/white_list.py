from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from typing import Callable, Awaitable, Dict, Any
from bot.users.models import User
from bot.users.dao import UserDAO
from aiogram.filters import CommandStart
from bot.database import async_session_maker



class VerificationMiddleware(BaseMiddleware):
    """
    Middleware для проверки верификационного статуса пользователя.
    Запрещает доступ ко всему функционалу, кроме команды /start
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id

        # Разрешенные команды 
        allowed_commands = ["/start"]

        # Если команда разрешена — пропускаем
        if event.text in allowed_commands:
            return await handler(event, data)

        # Проверяем статус пользователя
        logger.info(user_id)
        async with async_session_maker() as session:
            user = await UserDAO.find_by_telegram_id(session,int(user_id))
        logger.info(user)
        # Если пользователя нет в базе — запрещаем
        if not user:
            await event.answer("🚫 Вам запрещено пользоваться ботом. Пройдите верификацию через команду /start.")
            return

        # Если пользователь не верифицирован или заблокирован — запрещаем
        if user.verification_code == User.VerificationCode.NotVerified:
            await event.answer("🚫 Ваш аккаунт не верифицирован. Ожидайте одобрения администратора.")
            return
        if user.verification_code == User.VerificationCode.Blocked:
            async with async_session_maker() as session:
                admins:list[User] = await UserDAO.get_admins(session)
            for admin in admins:
                admin_link_msg = f"@{admin.username}\n" if admin.username else f'<a href="tg://user?id={admin.telegram_id}">администрация</a>\n'
            await event.answer(f"🚫 Ваш аккаунт заблокирован, если хотите это обжалобить напишите администрации: {admin_link_msg}")
            return

        # Если все в порядке, передаем управление дальше
        return await handler(event, data)
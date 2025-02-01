from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from app.config import admins
from bot.database import async_session_maker


class CheckIsAdmin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id in admins:
            return await handler(event, data) 
        else:
            await event.answer(
                "Только администраторы могут пользоваться этим функционалом"
            )

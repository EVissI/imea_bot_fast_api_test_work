from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from bot.admin.router import AdminCallback

def verified_user(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    logger.debug(AdminCallback.filter())
    kb.button(
        text="✅ Подтвердить",
        callback_data=AdminCallback(
            action="verified_user_yes",
            user_id=user_id
        ).pack()
    )
    kb.button(
        text="❌ Отклонить",
        callback_data=AdminCallback(
            action="verified_user_no",
            user_id=user_id
        ).pack()
    )
    kb.adjust(2)
    return kb.as_markup()
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.users.models import User

del_kbd = ReplyKeyboardRemove()


def main_keyboard(user_role: User.Role) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Проверить IMEI")
    kb.adjust(1)
    if user_role is User.Role.Admin:
        kb.button(text ='Список забаненных юзеров')
        kb.button(text = 'Список юзеров')
    return kb.as_markup(resize_keyboard=True)

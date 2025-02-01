from aiogram.filters import CommandObject, Command
from aiogram.filters.callback_data import CallbackData
from aiogram import F
from loguru import logger

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.router import Router
from bot.database import connection
from bot.users.models import User
from bot.users.dao import UserDAO
from bot.users.keyboards.markup_kb import main_keyboard
from bot.utils import update_user_ver_status, is_valid_telegram_id,split_message

TELEGRAM_ID_PATTERN = r"^[1-9]\d{6,9}$"
admin_router = Router()


class AdminCallback(CallbackData, prefix="admin"):
    action: str
    user_id: int = None


@admin_router.message(Command("unban"))
@connection()
async def cmd_unban_user(message: Message, command: CommandObject, session, **kwargs):
    try:
        user_id: str = command.args
        if not user_id:
            await message.answer(
                "После комманды /unban я ожидаю получить id пользователя в телеграмме"
            )
        elif not is_valid_telegram_id(user_id):
            await message.answer("Не верный формат ввода")
        else:
            user: User = await UserDAO.find_by_telegram_id(session, int(user_id))
            if not user:
                await message.answer("Пользователь с таким id не найден")
                return
            await update_user_ver_status(
                session=session,
                telegram_id=user_id,
                ver_status=User.VerificationCode.Verified,
            )
            await message.answer(f"Пользователь разблокирован")
            await message.bot.send_message(
                user_id,
                f"Поздравляем вас разблокировали!! Вы можете свободно пользоваться ботом",
                reply_markup=main_keyboard(user.role),
            )
    except Exception as e:
        logger.error(f"Произошла ошибка при выполнении комманды /unban - {e}")
        await message.answer(f"Произошла ошибка при выполнении комманды /unban - {e}")

@admin_router.message(Command("ban"))
@connection()
async def cmd_unban_user(message: Message, command: CommandObject, session, **kwargs):
    try:
        user_id: str = command.args
        if not user_id:
            await message.answer(
                "После комманды /ban я ожидаю получить id пользователя в телеграмме"
            )
        elif not is_valid_telegram_id(user_id):
            await message.answer("Не верный формат ввода")
        else:
            user: User = await UserDAO.find_by_telegram_id(session, int(user_id))
            if not user:
                await message.answer("Пользователь с таким id не найден")
                return
            await update_user_ver_status(
                session=session,
                telegram_id=user_id,
                ver_status=User.VerificationCode.Blocked,
            )
            await message.answer(f"Пользователь заблокирован")
            await message.bot.send_message(
                user_id,
                f"К сожалению администрация заблокировала вас",
            )
    except Exception as e:
        logger.error(f"Произошла ошибка при выполнении комманды /ban - {e}")
        await message.answer(f"Произошла ошибка при выполнении комманды /ban - {e}")


@admin_router.message(F.text == "Список забаненных юзеров")
@connection()
async def get_banned_user_list(message: Message, session, **kwargs):
    try:
        banned_users: list[User] = await UserDAO.get_banned_users(session)

        if not banned_users:
            await message.answer("Список заблокированных пользователей пуст.")
            return

        msg = "🔒 Заблокированные пользователи:\n"
        for user in banned_users:
            username = f"@{user.username}" if user.username else "Без имени"
            msg += f"👤 {username} (ID: {user.telegram_id})\n"
        answer = split_message(msg=msg, with_photo=False)
        for i in answer:
            await message.answer(i)
    except Exception as e:
        logger.error(f"Ошибка при получении списка юзеров - {e}")

@admin_router.message(F.text == "Список юзеров")
@connection()
async def get_banned_user_list(message: Message, session, **kwargs):
    try:
        users: list[User] = await UserDAO.get_all_users(session)

        if not users:
            await message.answer("Список пользователей пуст.")
            return

        msg = "Пользователи:\n"
        for user in users:
            username = f"@{user.username}" if user.username else "Без имени"
            msg += f"👤 {username} (ID: {user.telegram_id} Role: {user.role.value} Status:{user.verification_code.value})\n"
        answer = split_message(msg=msg, with_photo=False)
        for i in answer:
            await message.answer(i)
    except Exception as e:
        logger.error(f"Ошибка при получении списка юзеров - {e}")

@admin_router.callback_query(AdminCallback.filter())
@connection()
async def admin_callback(
    query: CallbackQuery, callback_data: AdminCallback, session, **kwargs
):
    user_id = callback_data.user_id
    logger.debug(f"Callback data: {callback_data}")
    try:
        if callback_data.action == "verified_user_yes":
            user:User = await UserDAO.find_by_telegram_id(session,int(user_id))
            await update_user_ver_status(
                session=session,
                telegram_id=user_id,
                ver_status=User.VerificationCode.Verified,
            )
            await query.answer("Пользователь верифицирован")
            await query.message.delete()
            await query.bot.send_message(
                user_id,
                "Ваш аккаунт верифицирован, можете пользоваться ботом",
                reply_markup=main_keyboard(user.role),
            )
            return
        if callback_data.action == "verified_user_no":

            await update_user_ver_status(
                session=session,
                telegram_id=user_id,
                ver_status=User.VerificationCode.Blocked,
            )
            await query.answer("Пользователь не верифицирован")
            await query.message.delete()
            await query.bot.send_message(
                user_id,
                "Сожалею, но ваш аккаунт был забанен. Дальнейшее пользование ботом не возможно",
            )
            return
    except Exception as e:
        logger.error(f"Ошибка при выполнении callback {callback_data.action}: {e}")
        await query.answer(
            "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже."
        )

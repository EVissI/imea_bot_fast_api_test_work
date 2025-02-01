from aiogram.filters import CommandObject, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.dispatcher.router import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import F

from loguru import logger
import aiohttp
import json

from bot.database import connection
from bot.admin.keyboards.inline_kb import verified_user
from bot.users.keyboards.markup_kb import main_keyboard, del_kbd
from bot.users.models import User
from bot.users.dao import UserDAO
from bot.users.schemas import TelegramIDModel, UserModel
from bot.utils import imei_validator

from app.config import admins, settings
from app.auth import create_jwt_token

user_router = Router()


class ImeiState(StatesGroup):
    Imei = State()


@user_router.message(CommandStart())
@connection()
async def cmd_start(message: Message, command: CommandObject, session, **kwargs):
    try:
        user_id = message.from_user.id
        user_info = await UserDAO.find_one_or_none(
            session=session, filters=TelegramIDModel(telegram_id=user_id)
        )

        if user_info:
            match user_info.verification_code:
                case User.VerificationCode.NotVerified:
                    msg = "Ваш аккаунт еще не проверен. Ожидайте, пока администратор проверит ваш аккаунт."
                    await message.answer(msg)
                    return
                case User.VerificationCode.Verified:
                    msg = "Мы уже проверили ваш аккаунт. Вы можете начать пользоваться ботом."
                    await message.answer(
                        msg, reply_markup=main_keyboard(user_info.role)
                    )
                    return
                case User.VerificationCode.Blocked:
                    admin_link_msg = ""
                    admins_list: list[User] = await UserDAO.get_admins(session)
                    for admin in admins_list:
                        admin_link_msg = (
                            f"@{admin.username}\n"
                            if admin.username
                            else f'<a href="tg://user?id={admin.telegram_id}">администрация</a>\n'
                        )
                    msg = (
                        "Ваш аккаунт заблокирован. Если хотите обжалобить свяжитесь с нами:\n"
                        + admin_link_msg
                    )
                    await message.answer(msg)
                    return

        if user_id in admins:
            values = UserModel(
                telegram_id=user_id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                verification_code=User.VerificationCode.Verified,
                role=User.Role.Admin,
            )
            await UserDAO.add(session=session, values=values)
            await message.answer(
                "Привет администрации", reply_markup=main_keyboard(User.Role.Admin)
            )
            return
        values = UserModel(
            telegram_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            verification_code=User.VerificationCode.NotVerified,
            role=User.Role.User,
        )
        await UserDAO.add(session=session, values=values)
        for admin_id in admins:
            try:
                user_info = f"Новый пользователь:\nID: {user_id}\nИмя: {message.from_user.full_name}"
                await message.bot.send_message(
                    admin_id, user_info, reply_markup=verified_user(user_id)
                )
            except Exception as e:
                logger.error(f"{e}")
        msg = f"Ожидайте, пока администратор проверит ваш аккаунт."
        await message.answer(msg)

    except Exception as e:
        logger.error(
            f"Ошибка при выполнении команды /start для пользователя {message.from_user.id}: {e}"
        )
        await message.answer(
            "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже."
        )


@user_router.message(F.text == "Проверить IMEI")
async def cmd_imei(message: Message, state: FSMContext):
    await message.answer("Введите imei", reply_markup=del_kbd)
    await state.set_state(ImeiState.Imei)


IMEI_PATTERN = r"^\d{15}$"


@user_router.message(F.text.regexp(IMEI_PATTERN), StateFilter(ImeiState.Imei))
@connection()
async def is_imei(message: Message, state: FSMContext, session, **kwargs):
    try:
        imei_number = message.text.strip()
        user: User = await UserDAO.find_by_telegram_id(
            session, int(message.from_user.id)
        )
        if not imei_validator(imei_number):
            await message.answer(
                "🚨 Ошибка: Введенный IMEI некорректен!\n",
                reply_markup=main_keyboard(user.role),
            )
            await state.clear()
            return
        imei_protected_url = f"{settings.BASE_SITE}/api/check-imei"
        token = create_jwt_token()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                imei_protected_url,
                params={"deviceId": imei_number},
                headers={"Authorization": f"Bearer {token}"},
            ) as imeo_api_response:
                if imeo_api_response.status != 201:
                    error_text = await imeo_api_response.text()
                    await message.answer(
                        f"❌ Ошибка запроса: {error_text}",
                        reply_markup=main_keyboard(user.role),
                    )
                    await state.clear()
                    return

                imei_data = await imeo_api_response.json()
                logger.info(f"API Response: {imei_data}")
                device_name = imei_data["properties"].get("deviceName", "Неизвестно")
                model_desc = imei_data["properties"].get("modelDesc", "Неизвестно")
                purchase_country = imei_data["properties"].get(
                    "purchaseCountry", "Неизвестно"
                )
                network_status = imei_data["properties"].get("network", "Неизвестно")
                warranty_status = imei_data["properties"].get(
                    "warrantyStatus", "Нет данных"
                )
                refurbished = (
                    "✅ Да" if imei_data["properties"].get("refurbished") else "❌ Нет"
                )
                fmi_on = (
                    "✅ Включен"
                    if imei_data["properties"].get("fmiOn")
                    else "❌ Отключен"
                )
                lost_mode = (
                    "✅ Да" if imei_data["properties"].get("lostMode") else "❌ Нет"
                )
                sim_lock = (
                    "✅ Есть" if imei_data["properties"].get("simLock") else "❌ Нет"
                )

                message_text = (
                    f"📱 **Данные устройства:**\n"
                    f"🔹 **Название:** {device_name}\n"
                    f"🔹 **Модель:** {model_desc}\n"
                    f"🌍 **Страна покупки:** {purchase_country}\n"
                    f"🔗 **Статус сети:** {network_status}\n"
                    f"🛡 **Гарантия:** {warranty_status}\n"
                    f"♻ **Восстановленный:** {refurbished}\n"
                    f"🔒 **iCloud (FMI):** {fmi_on}\n"
                    f"🚨 **Режим потери:** {lost_mode}\n"
                    f"📶 **SIM-лок:** {sim_lock}\n"
                )
                await message.answer(
                    message_text, reply_markup=main_keyboard(user.role)
                )
    except Exception as e:
        await message.answer(
            f"🚨 Ошибка при обработке запроса: {str(e)}",
            reply_markup=main_keyboard(user.role),
        )
        await state.clear()


@user_router.message(~F.text.regexp(IMEI_PATTERN), StateFilter(ImeiState.Imei))
@connection()
async def is_not_imei(message: Message, state: FSMContext, session, **kwargs):
    user: User = await UserDAO.find_by_telegram_id(session, int(message.from_user.id))
    await message.answer(
        "Это не похоже на Imei, попробуйте снова", reply_markup=main_keyboard(user.role)
    )
    await state.clear()

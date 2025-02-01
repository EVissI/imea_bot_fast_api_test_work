import re
from sqlalchemy.ext.asyncio import AsyncSession
from bot.users.schemas import TelegramIDModel, UserModel
from bot.users.dao import UserDAO
from bot.users.models import User

async def update_user_ver_status(session: AsyncSession, telegram_id: int, ver_status: User.VerificationCode):
    "обновление статуса пользователя"
    filters = TelegramIDModel(telegram_id=telegram_id)
    values = await UserDAO.find_one_or_none(session, filters)
    values = UserModel(
        telegram_id=values.telegram_id,
        username=values.username,
        first_name=values.first_name,
        last_name=values.last_name,
        verification_code=ver_status,
        role=values.role
    )
    return await UserDAO.update(session, filters, values)



TELEGRAM_ID_PATTERN = r'^[1-9]\d{6,9}$'
def is_valid_telegram_id(telegram_id: str) -> bool:
    return bool(re.match(TELEGRAM_ID_PATTERN, str(telegram_id)))

def imei_validator(imei: str) -> bool:
    imei = imei.replace("-", "")
    if len(imei) != 15 or not imei.isdigit():
        return False
    odd_sum = sum(int(imei[i]) for i in range(0, 15, 2))
    even_sum = 0
    for i in range(1, 15, 2):
        doubled = int(imei[i]) * 2
        even_sum += sum(int(digit) for digit in str(doubled))
    total_sum = odd_sum + even_sum
    return total_sum % 10 == 0

def split_message(msg: str, *, with_photo: bool) -> list[str]:
    """Split the text into parts considering Telegram limits."""
    parts = []
    while msg:
        # Determine the maximum message length based on
        # with_photo and whether it's the first iteration
        # (photo is sent only with the first message).
        if parts:
            max_msg_length = 4096
        elif with_photo:
            max_msg_length = 1024
        else:
            max_msg_length = 4096

        if len(msg) <= max_msg_length:
            # The message length fits within the maximum allowed.
            parts.append(msg)
            break

        # Cut a part of the message with the maximum length from msg
        # and find a position for a break by a newline character.
        part = msg[:max_msg_length]
        first_ln = part.rfind("\n")

        if first_ln != -1:
            # Newline character found.
            # Split the message by it, excluding the character itself.
            new_part = part[:first_ln]
            parts.append(new_part)

            # Trim msg to the length of the new part
            # and remove the newline character.
            msg = msg[first_ln + 1 :]
            continue

        # No newline character found in the message part.
        # Try to find at least a space for a break.
        first_space = part.rfind(" ")

        if first_space != -1:
            # Space character found. 
            # Split the message by it, excluding the space itself.
            new_part = part[:first_space]
            parts.append(new_part)
            
            # Trimming msg to the length of the new part
            # and removing the space.
            msg = msg[first_space + 1 :]
            continue

        # No suitable place for a break found in the message part.
        # Add the current part and trim the message to its length.
        parts.append(part)
        msg = msg[max_msg_length:]

    return parts
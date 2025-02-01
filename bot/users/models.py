import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger,Enum

from typing import Optional
from bot.database import Base


class User(Base):
    class VerificationCode(enum.Enum):
        NotVerified = 'NotVerified'
        Verified = 'Verified'
        Blocked = 'Blocked'
    class Role(enum.Enum):
        Admin = "Admin"
        User = "User"
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    verification_code: Mapped[VerificationCode] = mapped_column(Enum(VerificationCode), default=VerificationCode.NotVerified)
    role: Mapped[Role] = mapped_column(Enum(Role), server_default=Role.User.value)
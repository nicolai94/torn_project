from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.storage.models import IdUUIDPkMixin, UpdatedMixin, CreatedMixin
from src.storage.models.base import Base


class Wallet(Base, IdUUIDPkMixin, CreatedMixin, UpdatedMixin):
    address: Mapped[str]
    bandwidth: Mapped[int]
    energy: Mapped[int]
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=2))

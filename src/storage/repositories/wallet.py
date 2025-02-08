from decimal import Decimal

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage import Wallet
from src.storage.repositories.base import BaseRepository


class WalletRepository(BaseRepository[Wallet]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Wallet)

    async def add_wallet(
        self, address: str, bandwidth: int, energy: int, balance: Decimal
    ) -> Wallet:
        wallet = Wallet(
            address=address, bandwidth=bandwidth, energy=energy, balance=balance
        )
        self.session.add(wallet)

        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to add wallet {e}")

        await self.session.refresh(wallet)

        return wallet

    async def get_wallet_history(self, limit: int, offset: int) -> list[Wallet]:
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        instance = result.scalars().all()

        return instance

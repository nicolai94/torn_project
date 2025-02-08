from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from tronpy.keys import is_address

from src.api.api_v1.schemas.wallet import (
    AddressRequest,
    AddressResponse,
)
from src.api.exceptions import WrongTronAddressException
from src.integrations.tron.client import TronClient
from src.storage.repositories.wallet import WalletRepository


class WalletService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_address(self, params: AddressRequest) -> AddressResponse:
        if not is_address(params.address):
            raise WrongTronAddressException

        tron_client = TronClient()
        bandwidth, energy, balance = tron_client.get_account_resources(params.address)

        wallet_repo = WalletRepository(self.session)
        wallet = await wallet_repo.add_wallet(
            params.address, bandwidth, energy, balance
        )

        return AddressResponse(
            address=wallet.address,
            bandwidth=wallet.bandwidth,
            energy=wallet.energy,
            balance=wallet.balance,
        )

    async def get_wallet_history(
        self, limit: int, offset: int
    ) -> List[AddressResponse]:
        wallet_repo = WalletRepository(self.session)
        records = await wallet_repo.get_wallet_history(limit, offset)

        return [
            AddressResponse(
                address=record.address,
                bandwidth=record.bandwidth,
                energy=record.energy,
                balance=record.balance,
            )
            for record in records
        ]

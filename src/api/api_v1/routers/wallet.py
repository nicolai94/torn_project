from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.schemas.wallet import (
    AddressResponse,
    AddressRequest,
)
from src.services.wallet import WalletService
from src.storage.models.db_helper import db_connector

router = APIRouter()


@router.post("/address", response_model=AddressResponse)
async def get_address_info(
    params: AddressRequest, session: AsyncSession = Depends(db_connector.session_getter)
) -> AddressResponse:
    wallet_service = WalletService(session)

    return await wallet_service.add_address(params)


@router.get("/history", response_model=List[AddressResponse])
async def get_history(
    limit: int,
    offset: int,
    session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
) -> List[AddressResponse]:
    wallet_service = WalletService(session)

    return await wallet_service.get_wallet_history(limit, offset)

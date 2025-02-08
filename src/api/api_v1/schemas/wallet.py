from src.core.config import BaseSchema


class AddressRequest(BaseSchema):
    address: str


class AddressResponse(BaseSchema):
    address: str
    bandwidth: int
    energy: int
    balance: float


class WalletHistoryPaginationRequest(BaseSchema):
    limit: int
    offset: int

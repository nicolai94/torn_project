from starlette import status

from src.core.exceptions import CustomException


class AddressNotFoundException(CustomException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.code = "address_not_found"
        self.message = "Address not found"


class WrongTronAddressException(CustomException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.code = "wrong_tron_address"
        self.message = "Wrong TRON address"

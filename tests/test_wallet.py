from decimal import Decimal
from unittest.mock import patch

import pytest
from loguru import logger

from src.core.config import settings
from src.storage import Wallet
from src.storage.repositories.wallet import WalletRepository

pytestmark = pytest.mark.asyncio


@patch("src.integrations.tron.client.Tron.get_account_balance")
@patch("src.integrations.tron.client.Tron.get_account")
async def test_add_address(mocked_tron_get_account, mocked_get_balance, async_client):
    address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    mocked_tron_get_account.return_value = {
        "address": f"{address}",
        "balance": 123,
        "create_time": 123354465656,
        "net_window_size": 29283928390,
        "net_window_optimized": True,
        "account_resource": {
            "latest_consume_time_for_energy": 24234234234,
            "energy_window_size": 234234234,
            "energy_window_optimized": True,
        },
        "owner_permission": {
            "permission_name": "owner",
            "threshold": 1,
            "keys": [{"address": "wmrbnwebnr213123123", "weight": 1}],
        },
        "active_permission": [
            {
                "type": "Active",
                "id": 2,
                "permission_name": "active",
                "threshold": 1,
                "operations": "7fff1fc0033e3b00000000000000000000000000000000000000000000000000",
                "keys": [{"address": f"{address}", "weight": 1}],
            }
        ],
        "frozenV2": [{}, {"type": "ENERGY"}, {"type": "TRON_POWER"}],
        "assetV2": [
            {"key": "1000323", "value": 10},
            {"key": "1000016", "value": 1231231},
            {"key": "1000254", "value": 12312},
        ],
        "free_asset_net_usageV2": [
            {"key": "1", "value": 0},
            {"key": "2", "value": 0},
            {"key": "2", "value": 0},
        ],
        "asset_optimized": True,
    }
    mocked_get_balance.return_value = Decimal("123")

    data = {"address": f"{address}"}
    url = f"{settings.api.prefix}{settings.api.v1.prefix}/wallet/address"
    response = await async_client.post(
        url=url,
        json=data,
    )
    result = response.json()
    assert response.status_code == 200
    assert result["address"] == mocked_tron_get_account.return_value["address"]
    assert result["balance"] == mocked_get_balance.return_value
    assert result["bandwidth"] == 0
    assert result["energy"] == 0


async def test_get_address(async_client):
    data = {"limit": "10", "offset": "0"}
    url = f"{settings.api.prefix}{settings.api.v1.prefix}/wallet/history"
    logger.info(f"{url=}")
    response = await async_client.get(
        url=url,
        params=data,
    )

    assert response.status_code == 200


async def test_add_wallet_success(db_session):
    repository = WalletRepository(session=db_session)

    address = "test_address"
    bandwidth = 100
    energy = 50
    balance = Decimal("100.50")

    result = await repository.add_wallet(address, bandwidth, energy, balance)

    expected_wallet = Wallet(
        address=address, bandwidth=bandwidth, energy=energy, balance=balance
    )

    assert result.address == expected_wallet.address
    assert result.bandwidth == expected_wallet.bandwidth
    assert result.energy == expected_wallet.energy
    assert result.balance == expected_wallet.balance

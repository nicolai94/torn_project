from tronpy import Tron


class TronClient:
    def __init__(self, network: str = "nile"):
        self.client = Tron(network=network)
        self._account = None

    def _fetch_account(self, address: str):
        if not self._account:
            self._account = self.client.get_account(address)
        return self._account

    def get_account_resources(self, address: str):
        account = self._fetch_account(address)
        bandwidth = self._get_resource(account, "bandwidth")
        energy = self._get_resource(account, "energy")
        balance = self.balance(account)
        return bandwidth, energy, balance

    def _get_resource(self, account, resource_type: str):
        account_resource = getattr(account, "account_resource", None)

        if resource_type == "bandwidth":
            return self._get_bandwidth(account_resource, account)
        elif resource_type == "energy":
            return self._get_energy(account_resource, account)
        return 0

    def _get_bandwidth(self, account_resource, account):
        if account_resource and "free_net_limit" in account_resource and "net_usage" in account_resource:
            return account_resource["free_net_limit"] - account_resource["net_usage"]

        frozen_bandwidth = self._get_frozen_balance(account, "BANDWIDTH")
        return frozen_bandwidth

    def _get_energy(self, account_resource, account):
        if account_resource and "free_energy_limit" in account_resource and "energy_usage" in account_resource:
            return account_resource["free_energy_limit"] - account_resource["energy_usage"]

        frozen_energy = self._get_frozen_balance(account, "ENERGY")
        return frozen_energy

    @staticmethod
    def _get_frozen_balance(account, resource_type):
        frozen_balance = 0
        frozen_data = getattr(account, "frozenV2", [])
        for freeze in frozen_data:
            if freeze.get("type") == resource_type:
                frozen_balance = freeze.get("frozen_balance", 0)
        return frozen_balance

    def balance(self, account):
        return self.client.get_account_balance(account["address"]) if account else 0
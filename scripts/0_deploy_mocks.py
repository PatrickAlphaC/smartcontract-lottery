from brownie import (
    LinkToken,
    MockOracle,
    MockV3Aggregator,
    VRFCoordinatorMock,
    network,
)
from scripts.helpful_scripts import (
    NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
)

DECIMALS = 18
INITIAL_VALUE = 2000


def main():
    if network.show_active() in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks...")
        account = get_account()
        print("Deploying Mock Link Token...")
        link_token = LinkToken.deploy({"from": account})
        print("Deploying Mock Price Feed...")
        mock_price_feed = MockV3Aggregator.deploy(
            DECIMALS, INITIAL_VALUE, {"from": account}
        )
        print("Deploying Mock VRFCoordinator...")
        mock_vrf_coordinator = VRFCoordinatorMock.deploy(
            link_token.address, {"from": account}
        )
        print("Deploying Mock Oracle...")
        mock_oracle = MockOracle.deploy(link_token.address, {"from": account})
        print("Mocks Deployed!")
    else:
        print("Only deploy mocks to a non-forked local network!")

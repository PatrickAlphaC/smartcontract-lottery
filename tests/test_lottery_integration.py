import time

import pytest
from brownie import Lottery, exceptions, network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS

STATIC_SEED = 123
STATIC_RNG = 777


@pytest.fixture
def deploy_lottery_contract(
    get_eth_usd_price_feed_address,
    get_vrf_coordinator,
    get_link_token,
    get_keyhash,
):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange / Act
    lottery = Lottery.deploy(
        get_eth_usd_price_feed_address,
        get_vrf_coordinator.address,
        get_link_token.address,
        get_keyhash,
        {"from": get_account()},
    )
    # Assert
    assert lottery is not None
    return lottery


def test_can_pick_winner(
    deploy_lottery_contract, get_link_token, chainlink_fee, get_vrf_coordinator
):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery_contract
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    get_link_token.transfer(lottery.address, chainlink_fee * 2, {"from": account})
    transaction_receipt = lottery.endLottery(STATIC_SEED, {"from": account})
    requestId = transaction_receipt.events["RequestedRandomness"]["requestId"]
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

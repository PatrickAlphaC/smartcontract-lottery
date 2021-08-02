import time

import pytest
from brownie import Lottery, network
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.deploy_lottery import deploy_lottery

STATIC_RNG = 777


def test_can_pick_winner(chainlink_fee):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    get_contract("link_token").transfer(
        lottery.address, chainlink_fee * 2, {"from": account}
    )
    transaction_receipt = lottery.endLottery({"from": account})
    transaction_receipt.events["RequestedRandomness"]["requestId"]
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

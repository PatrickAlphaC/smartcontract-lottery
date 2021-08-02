from scripts.deploy_lottery import deploy_lottery
import pytest
from brownie import Lottery, exceptions, network
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

STATIC_RNG = 777


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    eth_usd_price = lottery.getLatestEthUsdPrice()
    entrance_fee = lottery.getEntranceFee()
    # 2000 is the inital of the eth / usd feed
    # usdEntryFee is 50
    # so we do 2000/1 is 50/x = 0.025 ETH == $50
    assert eth_usd_price == 2000000000000000000000
    assert entrance_fee == 25000000000000000


# 2500000 00000000 0000000000
# 2000 00 000000000000000000
def test_cant_enter_lottery_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.players(1) == account


def test_can_end_lottery(chainlink_fee):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
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
    assert transaction_receipt.events["RequestedRandomness"]["requestId"] is not None


def test_can_pick_winner(chainlink_fee):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
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
    requestId = transaction_receipt.events["RequestedRandomness"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, STATIC_RNG, lottery.address, {"from": account}
    )
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

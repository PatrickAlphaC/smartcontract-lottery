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
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
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


def test_get_entrance_fee(deploy_lottery_contract):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery_contract
    eth_usd_price = lottery.getLatestEthUsdPrice()
    price = lottery.getEntranceFee()
    # 2000 is the inital of the eth / usd feed
    # usdEntryFee is 50
    # so we do 2000/1 is 50/x = 0.025 ETH == $50
    assert eth_usd_price == 2000000000000000000000
    assert price == 25000000000000000


def test_cant_enter_lottery_unless_started(deploy_lottery_contract):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery_contract
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery(deploy_lottery_contract):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery_contract
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.players(1) == account


def test_can_end_lottery(deploy_lottery_contract, get_link_token, chainlink_fee):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery_contract
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    get_link_token.transfer(lottery.address, chainlink_fee * 2, {"from": account})
    transaction_receipt = lottery.endLottery(STATIC_SEED, {"from": account})
    assert transaction_receipt.events["RequestedRandomness"]["requestId"] is not None


def test_can_pick_winner(
    deploy_lottery_contract, get_link_token, chainlink_fee, get_vrf_coordinator
):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery_contract
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    get_link_token.transfer(lottery.address, chainlink_fee * 2, {"from": account})
    transaction_receipt = lottery.endLottery(STATIC_SEED, {"from": account})
    requestId = transaction_receipt.events["RequestedRandomness"]["requestId"]
    get_vrf_coordinator.callBackWithRandomness(
        requestId, STATIC_RNG, lottery.address, {"from": account}
    )
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

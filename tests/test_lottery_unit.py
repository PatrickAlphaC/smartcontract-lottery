from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    get_contract,
)
from brownie import exceptions
from web3 import Web3
import pytest


def test_get_entrance_fee(check_local_blockchain_envs, lottary_contract):
    # Arrange (by fixtures)

    # Act
    # 2,000 eth / usd
    # usdEntryFee is 50
    # 2000/1 == 50/x == 0.025
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottary_contract.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started(check_local_blockchain_envs, lottary_contract):
    # Arrange (by fixtures)

    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottary_contract.enter(
            {"from": get_account(), "value": lottary_contract.getEntranceFee()}
        )


def test_can_start_and_enter_lottery(check_local_blockchain_envs, lottary_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottary_contract.startLottery({"from": account})
    # Act
    lottary_contract.enter(
        {"from": account, "value": lottary_contract.getEntranceFee()}
    )
    # Assert
    assert lottary_contract.players(0) == account


def test_can_end_lottery(check_local_blockchain_envs, lottary_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottary_contract.startLottery({"from": account})
    lottary_contract.enter(
        {"from": account, "value": lottary_contract.getEntranceFee()}
    )
    fund_with_link(lottary_contract)
    lottary_contract.endLottery({"from": account})
    assert lottary_contract.lottery_state() == 2


def test_can_pick_winner_correctly(check_local_blockchain_envs, lottary_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottary_contract.startLottery({"from": account})
    lottary_contract.enter(
        {"from": account, "value": lottary_contract.getEntranceFee()}
    )
    lottary_contract.enter(
        {"from": get_account(index=1), "value": lottary_contract.getEntranceFee()}
    )
    lottary_contract.enter(
        {"from": get_account(index=2), "value": lottary_contract.getEntranceFee()}
    )
    fund_with_link(lottary_contract)
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottary_contract.balance()
    transaction = lottary_contract.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottary_contract.address, {"from": account}
    )
    # 777 % 3 = 0
    assert lottary_contract.recentWinner() == account
    assert lottary_contract.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery

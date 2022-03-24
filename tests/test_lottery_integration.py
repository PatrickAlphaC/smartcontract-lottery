from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
)
import time


def test_can_pick_winner(check_local_blockchain_envs, lottary_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottary_contract.startLottery({"from": account})
    lottary_contract.enter(
        {"from": account, "value": lottary_contract.getEntranceFee()}
    )
    lottary_contract.enter(
        {"from": account, "value": lottary_contract.getEntranceFee()}
    )
    fund_with_link(lottary_contract)
    lottary_contract.endLottery({"from": account})
    time.sleep(180)
    assert lottary_contract.recentWinner() == account
    assert lottary_contract.balance() == 0

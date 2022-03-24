from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
)
import time


def test_can_pick_winner(check_local_blockchain_envs, lottary):
    # Arrange (by fixtures)

    account = get_account()
    lottary.startLottery({"from": account})
    lottary.enter({"from": account, "value": lottary.getEntranceFee()})
    lottary.enter({"from": account, "value": lottary.getEntranceFee()})
    fund_with_link(lottary)
    lottary.endLottery({"from": account})
    time.sleep(180)
    assert lottary.recentWinner() == account
    assert lottary.balance() == 0

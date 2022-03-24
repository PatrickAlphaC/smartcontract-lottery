from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
)
import time


def test_can_pick_winner(check_local_blockchain_envs, lottery_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    fund_with_link(lottery_contract)
    lottery_contract.endLottery({"from": account})
    time.sleep(180)
    assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() == 0

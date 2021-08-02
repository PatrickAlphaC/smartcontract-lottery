#!/usr/bin/python3
from brownie import Lottery, accounts, config, network
from scripts.helpful_scripts import get_contract, get_account, fund_with_link
import time

lottery_enum = {0: "OPEN", 1: "CLOSED", 2: "CALCULATING_WINNER"}


def deploy_lottery():
    account = get_account()
    # level up get_account for all 3 though
    print(network.show_active())
    return Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    transaction = fund_with_link(lottery.address)
    transaction.wait(1)
    transaction_2 = lottery.startLottery({"from": account})
    transaction_2.wait(1)
    print(f"The lottery is currently {lottery_enum[lottery.lottery_state()]}")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    transaction_2 = lottery.enter({"from": account, "value": value})
    transaction_2.wait(1)
    print(f"{account} has entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    print(f"The previous winner is {lottery.recentWinner()}, let's get a new one!")
    transaction = lottery.endLottery({"from": account})
    transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    # start_lottery()
    # enter_lottery()
    # end_lottery()

#!/usr/bin/python3
from brownie import Lottery, accounts, config, network
from scripts.helpful_scripts import fund_with_link

lottery_enum = {0: "OPEN", 1: "CLOSED", 2: "CALCULATING_WINNER"}


def main():
    account = accounts.add(config["wallets"]["from_key"])
    lottery = Lottery[len(Lottery) - 1]
    transaction = fund_with_link(lottery.address)
    transaction.wait(1)
    transaction_2 = lottery.startLottery({"from": account})
    transaction_2.wait(1)
    print(f"The lottery is currently {lottery_enum[lottery.lottery_state()]}")

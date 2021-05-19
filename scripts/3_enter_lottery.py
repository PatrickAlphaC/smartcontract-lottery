#!/usr/bin/python3
from brownie import Lottery, accounts, config
from scripts.helpful_scripts import fund_with_link


def main():
    account = accounts.add(config["wallets"]["from_key"])
    lottery = Lottery[len(Lottery) - 1]
    value = lottery.getEntranceFee() + 100000000
    transaction_2 = lottery.enter({"from": account, "value": value})
    transaction_2.wait(1)
    print(f"{account} has entered the lottery!")

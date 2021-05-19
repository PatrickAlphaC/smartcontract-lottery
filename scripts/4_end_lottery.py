#!/usr/bin/python3
from brownie import Lottery, accounts, config
import time

STATIC_SEED = 123


def main():
    account = accounts.add(config["wallets"]["from_key"])
    lottery = Lottery[len(Lottery) - 1]
    print(f"The previous winner is {lottery.recentWinner()}, let's get a new one!")
    transaction = lottery.endLottery(STATIC_SEED, {"from": account})
    transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")

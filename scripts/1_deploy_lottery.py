#!/usr/bin/python3
from brownie import Lottery, accounts, config, network


def main():
    account = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    verify = (
        config["networks"][network.show_active()]["verify"]
        if config["networks"][network.show_active()].get("verify")
        else False
    )
    return Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=verify,
    )

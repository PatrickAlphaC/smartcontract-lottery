from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import network
from scripts.deploy_lottery import deploy_lottery
import pytest


@pytest.fixture()
def check_local_blockchain_envs():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()


@pytest.fixture()
def lottery_contract():
    return deploy_lottery()

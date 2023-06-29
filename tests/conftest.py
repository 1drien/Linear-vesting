import pytest
from brownie import accounts, MyToken, LinearVesting


@pytest.fixture(scope="module")
def my_token():
    accounts_param = {"from": accounts[0]}
    initial_supply = 1000000
    return MyToken.deploy(initial_supply, accounts_param)


@pytest.fixture(scope="module")
def vesting(my_token):
    accounts_param = {"from": accounts[0]}
    duration = 180
    cliff = 90
    return LinearVesting.deploy(my_token.address, duration, cliff, accounts_param)

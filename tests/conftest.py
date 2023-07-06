import pytest
from brownie import accounts, MyToken, LinearVesting


@pytest.fixture(scope="module")
def my_token():
    initial_procurement = 1000000
    return MyToken.deploy(initial_procurement, {"from": accounts[0]})


@pytest.fixture(scope="module")
def vesting(my_token):
    accounts_parameters = {"from": accounts[0]}
    duration_of_vesting = 1800
    cliff_of_vesting = 900
    return LinearVesting.deploy(
        my_token.address, duration_of_vesting, cliff_of_vesting, accounts_parameters
    )

@pytest.fixture(scope="module")
def accounts_parameters():
    return {"from": accounts[0]}


@pytest.fixture(scope="module")
def receiver():
    return accounts[1]


@pytest.fixture
def new_vesting(my_token, accounts_parameters):
    duration = 1800
    cliff = 900
    return LinearVesting.deploy(my_token.address, duration, cliff, accounts_parameters)

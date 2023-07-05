import pytest
from brownie import accounts, MyToken, LinearVesting


@pytest.fixture(scope="module")
def my_token():
    initial_procurement = 1000000
    return MyToken.deploy(initial_procurement, {"from": accounts[0]})


@pytest.fixture(scope="module")
def vesting(my_token):
    accounts_parameters = {"from": accounts[0]}
    duration_of_vesting = 180
    cliff_of_vesting = 90
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
def new_vesting(my_token):
    accounts_param = {"from": accounts[0]}
    duration = 180
    cliff = 90
    return LinearVesting.deploy(
        my_token.address,
        duration,
        cliff,
        accounts_param,
    )


@pytest.fixture(scope="function")
def amount(new_vesting, receiver):
    return new_vesting.linear_vesting_details(receiver).amount()

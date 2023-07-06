# import my contract
from brownie import MyToken, LinearVesting, accounts


def main():
    # params settins in a dictionnary
    settings = {"duration": 180, "cliff": 90, "initial_supply": 1000000}
    # account parameters
    account = accounts[0]
    account_params = {"from": account}

    # Deploy the token
    my_token = MyToken.deploy(settings["initial_supply"], account_params)
    print("Token:", my_token.address)

    # Deploy the vesting contract
    linear_vesting = LinearVesting.deploy(
        my_token.address, settings["duration"], settings["cliff"], account_params
    )
    print("Vesting:", linear_vesting.address)

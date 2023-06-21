from brownie import MyToken, LinearVesting, accounts


def main():
    account = accounts[0]

    # Deploy the token
    initialSupply = 1000000 * 10**18
    myToken = MyToken.deploy(initialSupply, {"from": account})

    # Deploy the vesting contract
    duration = 180
    cliff = 90  # test cliff
    linearVesting = LinearVesting.deploy(
        myToken.address, duration, cliff, {"from": account}
    )
    print("Token:", myToken.address)
    print("Vesting:", linearVesting.address)

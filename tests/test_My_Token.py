from brownie import MyToken, accounts


def test_deploy_MyToken():
    # arrange
    account_params = {"from": accounts[0]}
    initial_supply = 1000000 * 10**18
    # Act

    MyToken_instance = MyToken.deploy(initial_supply, account_params)

    # assert
    assert (
        MyToken_instance.totalSupply() == initial_supply
    )  # all tokens are allocated to the deployer account when the contract is created; this should be equal to the initial offer.


# check that the deployment account balance has decreased
# and that the receiver account balance has increased by the appropriate amount.
def test_transfer():
    account_params = {"from": accounts[0]}
    initial_supply = 1000000 * 10**18
    receiver = accounts[1]
    transfer_amount = 5000000000

    MyToken_instance = MyToken.deploy(initial_supply, account_params)
    # Act
    MyToken_instance.transfer(receiver, transfer_amount, account_params)
    # Assert
    assert MyToken_instance.balanceOf(receiver) == transfer_amount

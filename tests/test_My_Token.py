from brownie import MyToken, accounts

# test 1: test_deploy_MyToken
# test 2: test_transfer: check that the deployment account balance has decreased and that the receiver account balance has increased by the appropriate amount.


def test_deploy_MyToken(my_token):
    assert (
        my_token.totalSupply() == 1000000
    )  # all tokens are allocated to the deployer account when the contract is created; this should be equal to the initial offer.


def test_transfer(my_token):
    receiver = accounts[1]
    transfer_amount = 500000
    account_params = {"from": accounts[0]}
    # Act
    my_token.transfer(receiver, transfer_amount, account_params)
    # Assert
    assert my_token.balanceOf(receiver) == transfer_amount

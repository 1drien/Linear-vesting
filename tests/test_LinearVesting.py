from brownie import accounts

#   test_lock : This test verifies that tokens can be locked for a defined period.
# 	test_transfer_tokens: This test verifies that the contract can transfer tokens.
# 	test_set_receiver : This test verifies that a beneficiary can be named.
# 	test_withdraw : This test verifies that correct removal can be performed after the period


def test_lock(my_token, vesting):
    # Arrange
    amount = 1000
    account = accounts[0]
    receiver = accounts[1]

    accounts_param = {"from": account}

    # authorize the vesting contract to move the tokenss
    my_token.approve(vesting.address, amount, accounts_param)
    # act
    vesting.lock(receiver, amount, accounts_param)

    # Assert
    assert vesting.receiver() == receiver
    assert vesting.amount() == amount


def test_transfer_tokens(my_token, vesting):
    # Arrange
    amount = 1000
    accounts_params = {"from": receiver}
    receiver = accounts[1]
    # The receiver attempts to withdraw the tokens
    vesting.withdraw(accounts_params)
    # The balance of the receiver should now be equal to the amount
    assert my_token.balanceOf(receiver) == amount


def test_set_receiver():
    # Arrange
    amount = 1000
    accounts_params = {"from": receiver}
    receiver = accounts[1]

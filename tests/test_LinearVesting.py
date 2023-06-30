from brownie import accounts, reverts, chain

#   test_lock : This test verifies that tokens can be locked for a defined period.
# 	test_transfer_tokens: This test verifies that the contract can transfer tokens.
#   test_withdraw_before_cliff
#   test_total_vesting_amount


def lock_tokens(my_token, new_vesting, receiver, amount, accounts_parameters):
    my_token.approve(new_vesting.address, amount, accounts_parameters)
    new_vesting.lock(receiver, amount, accounts_parameters)


def test_lock(my_token, new_vesting, receiver, amount, accounts_parameters):
    lock_tokens(my_token, new_vesting, receiver, amount, accounts_parameters)
    amount_vesting = new_vesting.amount()
    assert new_vesting.receiver() == receiver
    assert amount_vesting == amount


def test_lock_amount(my_token, new_vesting, receiver, amount, accounts_parameters):
    lock_tokens(my_token, new_vesting, receiver, amount, accounts_parameters)
    assert new_vesting.amount() == amount


def test_transfer_tokens(my_token, new_vesting, receiver, amount, accounts_parameters):
    my_token.approve(new_vesting.address, amount, accounts_parameters)
    new_vesting.lock(receiver, amount, accounts_parameters)

    # The receiver attempts to withdraw the tokens
    with reverts("Nothing can be withdrawn before the cliff"):
        new_vesting.withdraw({"from": receiver})
    # after one hour
    chain.mine()
    chain.sleep(3600)
    new_vesting.withdraw({"from": receiver})
    assert my_token.balanceOf(receiver) == amount


def test_of_vesting_duration(new_vesting):
    # arrange
    duration_of_vesting_expected = 180
    # act
    actual_duration_of_vesting = new_vesting.duration()
    # assert
    assert duration_of_vesting_expected == actual_duration_of_vesting


def test_of_cliff(new_vesting):
    # arrange
    cliff_expected = 90
    # act
    cliff_of_vesting = new_vesting.cliff()
    # assert
    assert cliff_expected == cliff_of_vesting


def test_of_withdraw_before__the_cliff(
    my_token, new_vesting, receiver, amount, accounts_parameters
):
    my_token.approve(new_vesting.address, amount, accounts_parameters)
    new_vesting.lock(receiver, amount, accounts_parameters)

    with reverts("Nothing can be withdrawn before the cliff"):
        new_vesting.withdraw({"from": receiver})
    assert my_token.balanceOf(receiver) == amount

from brownie import accounts, reverts, chain

#   test_lock : This test verifies that tokens can be locked for a defined period.
# 	test_transfer_tokens: This test verifies that the contract can transfer tokens.
#   test_withdraw_before_cliff
#   test_total_vesting_amount

amount_to_be_vested = 1000

def get_amount(vesting, receiver):
    return vesting.linearVestingDetails(receiver)[-2]

def get_liner_details(vesting, receiver):
    return {
        "start":vesting.linearVestingDetails(receiver)[0],
        "amount":vesting.linearVestingDetails(receiver)[1],
        "totalAmount":vesting.linearVestingDetails(receiver)[2]
    }

def lock_tokens(my_token, new_vesting, receiver, amount, accounts_parameters):
    my_token.approve(new_vesting.address, amount, accounts_parameters)
    new_vesting.lock(receiver, amount, accounts_parameters)


def test_lock(my_token, new_vesting, receiver, accounts_parameters):
    lock_tokens(my_token, new_vesting, receiver, amount_to_be_vested, accounts_parameters)
    details_vesting = get_liner_details(new_vesting, receiver)
    assert details_vesting["amount"] == amount_to_be_vested

def test_limit_lock(my_token, new_vesting, receiver, accounts_parameters):
    with reverts("The amount to lock must be positive"):
        lock_tokens(my_token, new_vesting, receiver, 0, accounts_parameters)
    lock_tokens(my_token, new_vesting, receiver, amount_to_be_vested, accounts_parameters)
    with reverts("Already locked"):
        lock_tokens(my_token, new_vesting, receiver, amount_to_be_vested, accounts_parameters)
    assert new_vesting.linearVestingDetails(receiver)[-2] == amount_to_be_vested

def test_limit_withdraw(my_token, new_vesting, receiver, accounts_parameters):
    my_token.approve(new_vesting.address, amount_to_be_vested, accounts_parameters)
    new_vesting.lock(receiver, amount_to_be_vested, accounts_parameters)
    unrelated_user = accounts[3]
    unrelated_user_params = {"from": unrelated_user}
    # The receiver attempts to withdraw the tokens
    with reverts("Nothing can be withdrawn before the cliff"):
        new_vesting.withdraw({"from": receiver})
    # after one hour
    chain.mine()
    chain.sleep(3600)
    with reverts("You are not authorized to release the tokens"):
        new_vesting.withdrawFor(receiver, unrelated_user_params)

def test_lock_amount(my_token, new_vesting, receiver, accounts_parameters):
    lock_tokens(my_token, new_vesting, receiver, amount_to_be_vested, accounts_parameters)
    assert get_amount(new_vesting, receiver) == amount_to_be_vested


def test_transfer_tokens(my_token, new_vesting, receiver, accounts_parameters):
    my_token.approve(new_vesting.address, amount_to_be_vested, accounts_parameters)
    new_vesting.lock(receiver, amount_to_be_vested, accounts_parameters)

    # The receiver attempts to withdraw the tokens
    with reverts("Nothing can be withdrawn before the cliff"):
        new_vesting.withdraw({"from": receiver})
    # after one hour
    chain.mine()
    chain.sleep(3600)
    new_vesting.withdraw({"from": receiver})
    assert my_token.balanceOf(receiver) == amount_to_be_vested


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


def test_of_withdraw_before_the_cliff(
    my_token, new_vesting, receiver, accounts_parameters
):
    my_token.approve(new_vesting.address, amount_to_be_vested, accounts_parameters)
    new_vesting.lock(receiver, amount_to_be_vested, accounts_parameters)

    with reverts("Nothing can be withdrawn before the cliff"):
        new_vesting.withdraw({"from": receiver})
    assert my_token.balanceOf(receiver) == amount_to_be_vested


def test_withdraw_before_end(my_token, new_vesting, receiver, accounts_parameters):
    my_token.approve(new_vesting.address, amount_to_be_vested, accounts_parameters)
    new_vesting.lock(receiver, amount_to_be_vested, accounts_parameters)
    # after one hour
    chain.mine()
    chain.sleep(1800)

    new_vesting.withdraw({"from": receiver})
    assert my_token.balanceOf(receiver) == amount_to_be_vested * 1/2

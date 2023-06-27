from brownie import accounts


def test_lock():
    # Arrange
    settings = {"duration": 180, "cliff": 90, "amount": 1000}
    account = accounts[0]
    receiver = accounts[1]
    token_address = "adresse_du_token"
    accounts_param = {"from": account}

    vesting_contract = LinearVesting.deploy(
        token_address, settings["duration"], settings["cliff"], accounts_param
    )

    # Act
    vesting_contract.lock(receiver, settings["amount"], accounts_param)

    # Assert
    assert vesting_contract.receiver() == receiver
    assert vesting_contract.amount() == settings["amount"]

from brownie import MyToken, accounts


def test_deploy_MyToken():
    # arrange
    account = accounts[0]
    initial_supply = 1000000 * 10**18
    # Act
    MyToken_instance = MyToken.deploy(initial_supply, {"from": account})

    # assert
    assert (
        MyToken_instance.totalSupply() == initial_supply
    )  # all tokens are allocated to the deployer account when the contract is created; this should be equal to the initial offer.


# vérifier que le solde du compte de déploiement a diminué
# et que le solde du compte récepteur a augmenté du montant approprié.
def test_transfer():
    account = accounts[0]
    initial_supply = 1000000 * 10**18
    receiver = accounts[1]
    transfer_amount = 5000000000
    MyToken_instance = MyToken.deploy(initial_supply, {"from": account})
    # Act
    MyToken_instance.transfer(receiver, transfer_amount, {"from": account})
    # Assert
    assert MyToken_instance.balanceOf(receiver) == transfer_amount

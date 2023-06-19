// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title LinearVesting
 * @dev
 */
contract LinearVesting is Ownable {
    IERC20 token;
    uint256 public start; // quand le vesting commence
    uint256 public cliff; // Période en seconde
    uint256 public duration; // durée du vesting
    address receiver; // destinataire
    uint256 amount; // nombre de tokkens envoyés
    uint256 totalAmount; // montant total des tokens bloqués dans le contract

    //ajouter event

    constructor(address _token, uint256 _duration, uint256 _cliff) {
        require(_duration > 0, "La duree doit etre positive");
        require(
            _duration >= _cliff,
            "cliff ne peut etre superieur a la duree du vesting"
        );
        cliff = _cliff;
        token = IERC20(_token);
        //on initialise pas start dans le constructeur pour s'assurer que la période de vesting commence après que les tokens verouillés
        duration = _duration;
    }

    /**
     * @dev imobiliser tokkens a periode determinée
     * @param _from description from
     * @param _receiver description receiver
     */
    function lock(
        address _from,
        address _receiver,
        uint256 _amount
    ) public onlyOwner {
        // Vérifier que le montant à verrouiller est positif
        require(_amount > 0, "Le montant a verrouiller doit etre positif");

        require(totalAmount == 0, "deja locker"); // peut etre verrouillé qu'une seule fois

        token.transferFrom(_from, address(this), _amount); //transférer les tokens du propriétaire original (_from) vers le contrat de vesting (address(this)).

        receiver = _receiver;
        amount = _amount;
        start = block.timestamp;
        totalAmount = _amount;
    }

    //Pas de paramètres
    /**
     * @dev libération linéaire des tokens selon letemps fixé
     *
     *
     */
    function release() external {
        require(block.timestamp >= start, "Vesting n'est pas commence");
        require(
            block.timestamp >= start + cliff,
            "Avant le cliff rien ne peut etre retire"
        ); //le délai de vesting a commencé.
        require(
            msg.sender == receiver || msg.sender == owner(),
            "Vous n'etes pas autorise a liberer les tokens"
        );
        // calcule du pourcentage de temps depuis le debut du vesting
        uint256 pourcentageTime = (block.timestamp - start) / duration;

        //combien de tokens sont disponibles pour être libérés en fonction du temps écoulé depuis le début du vesting.
        uint256 totalAmount = pourcentageTime * amount;
        //Transférer ces tokens au bénéficiaire.

        token.transfer(receiver, totalAmount); //
    }
}

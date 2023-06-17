// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LinearVesting is Ownable {
    IERC20 token;
    uint256 public start; // quand le vesting commence
    uint256 public cliff; // Période en seconde
    uint256 public duration; // durée du vesting
    address receiver; // destinataire
    uint256 amount; // nombre de tokkens envoyés
    uint256 expiry;
    bool public locked = false;
    bool public claimed = false;

    //ajouter event

    constructor(
        address _token,
        uint256 _start,
        uint256 _duration,
        uint256 _cliff
    ) {
        require(_duration > 0, "Duration must be positive");
        require(
            _duration >= _cliff,
            "cliff ne peut être supérieur a la durée du vesting"
        );
        cliff = _cliff;
        token = IERC20(_token);
        //on initialise pas start dans le constructeur pour s'assurer que la période de vesting commence après que les tokens verouillés
        duration = _duration;
    }

    //imobiliser tokkens a periode determinée
    function lock(
        address _from,
        address _receiver,
        uint256 _amount,
        uint256 _expiry
    ) public onlyOwner {
        // Vérifier que le montant à verrouiller est positif
        require(_amount > 0, "Le montant à verrouiller doit être positif");
        require(!locked, "We have alrady locked tokens");
        /*require(totalAmount == 0, "Already locked");*/ // peut etre verrouillé qu'une seule fois
        token.transferFrom(msg.sender, address(this), _amount);

        receiver = _receiver;
        expiry = _expiry;
        amount = _amount;
        start = block.timestamp;
    }

    // libération des tokens selon letemps fixé

    function release() external {
        require(!claimed, "tokens have been claimed");
        require(block.timestamp >= start, "Vesting n'est pas commencé");
        claimed = true;
        //libération es tokens linéaire
        token.transfer(reciver, amount);
    }
}

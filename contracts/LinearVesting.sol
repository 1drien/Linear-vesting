// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LinearVesting {
    IERC20 token;
    uint256 public start; // cliff
    uint256 public duration;
    address receiver; // destinataire
    uint256 amount; // nombre de tokkens envoyés
    uint256 expiry;
    bool public locked = false;
    bool public claimed = false;

    //ajouter event

    constructor(address _token, uint256 _start, uint256 _duration) {
        require(address(_token) != address(0), "Token is the zero address");
        //require(_start > block.timestamp, "Start must be in the future");
        require(_duration > 0, "Duration must be positive");

        token = IERC20(_token);
        start = _start;
        duration = _duration;
        owner = msg.sender;
    }

    //imobiliser tokkens a periode determinée
    function lock(
        address _from,
        address _receiver,
        uint256 _amount,
        uint256 _expiry
    ) public {
        // Vérifier que le montant à verrouiller est positif
        require(_amount > 0, "Le montant à verrouiller doit être positif");
        require(
            msg.sender == owner,
            "Seul le propriétaire peut verrouiller des tokens"
        );
        require(!locked, "We have alrady locked tokens");

        token.transferFrom(_from, address(this), _amount);
        receiver = _receiver;
    }

    // libération des tokens selon letemps fixé
}

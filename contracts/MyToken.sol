// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(uint256 initialSupply) public ERC20("MyToken", "MTK") {
        _mint(msg.sender, initialSupply); // the initial number of tokens, internal function from ERC20
    }
}

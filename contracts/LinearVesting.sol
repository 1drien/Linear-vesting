// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title LinearVesting
 * @dev Linear vesting contract
 */
contract LinearVesting is Ownable {
    IERC20 public immutable token;
    uint256 public start; // when the vesting starts
    uint256 public cliff; // period in seconds
    uint256 public duration; // vesting duration
    address public receiver; // recipient
    uint256 public amount; // number of tokens to be sent
    uint256 public totalAmount; // total amount of tokens locked in the contract

    constructor(address _token, uint256 _duration, uint256 _cliff) {
        require(_duration > 0, "Duration must be positive");
        require(
            _duration >= _cliff,
            "Cliff cannot be greater than the vesting duration"
        );

        cliff = _cliff;
        token = IERC20(_token);
        // start is not initialized in the constructor to ensure that the vesting period starts after the locked tokens
        duration = _duration;
    }

    /**
     * @dev Lock tokens for a specified period
     * @param _receiver description receiver
     * @param _amount number of token to lock
     */
    function lock(address _receiver, uint256 _amount) public onlyOwner {
        // Check that the amount to be locked is positive
        require(_amount > 0, "The amount to lock must be positive");

        // can only be locked once
        require(totalAmount == 0, "Already locked");

        token.transferFrom(msg.sender, address(this), _amount);

        receiver = _receiver;
        amount = _amount;
        start = block.timestamp;
        totalAmount = _amount;
    }

    /**
     * @dev Linear release of tokens according to the set time
     * No parameters
     */
    function withdraw() external {
        require(block.timestamp >= start, "Vesting has not started");
        require(
            block.timestamp >= start + cliff,
            "Nothing can be withdrawn before the cliff"
        ); // the vesting delay has started
        require(
            msg.sender == receiver || msg.sender == owner(),
            "You are not authorized to release the tokens"
        );

        // If the vesting period is over, allow the beneficiary to withdraw all tokens
        if (block.timestamp >= start + duration) {
            token.transfer(receiver, totalAmount);
            totalAmount = 0;
        } else {
            // calculate the percentage of time since the start of vesting
            uint256 timePercentage = (block.timestamp - start) / duration;

            // how many tokens are available to be released based on the time elapsed since the start of vesting
            uint256 availableAmount = timePercentage * amount;

            // Check if the totalAmount is greater than the availableAmount
            require(
                totalAmount >= availableAmount,
                "No tokens available for release"
            );

            // Update the total amount
            totalAmount -= availableAmount;

            // Transfer these tokens to the beneficiary
            token.transfer(receiver, availableAmount);
        }
    }
}

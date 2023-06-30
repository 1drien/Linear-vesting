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
    uint256 public cliff; // period in seconds
    uint256 public duration; // vesting duration

    struct Linear_vesting_details {
        uint256 start; // when the vesting starts
        address receiver; // recipient
        uint256 amount; // number of the tokens to be sent
        uint256 totalAmount; // total amount of tokens locked in the contract
    }

    mapping(address => Linear_vesting_details) public linear_vesting_details;

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
        require(
            linear_vesting_details[msg.sender].totalAmount == 0,
            "Already locked"
        );

        token.transferFrom(msg.sender, address(this), _amount);

        linear_vesting_details[_receiver] = Linear_vesting_details(
            block.timestamp,
            _receiver,
            _amount,
            _amount
        );
    }

    /**
     * @dev Linear release of tokens according to the set time
     * No parameters
     */
    function withdraw() external {
        require(
            block.timestamp >= linear_vesting_details[msg.sender].start,
            "Vesting has not started"
        );
        require(
            block.timestamp >= linear_vesting_details[msg.sender].start + cliff,
            "Nothing can be withdrawn before the cliff"
        ); // the vesting delay has started
        require(
            msg.sender == linear_vesting_details[msg.sender].receiver ||
                linear_vesting_details[msg.sender].receiver == owner(),
            "You are not authorized to release the tokens"
        );

        // If the vesting period is over, allow the beneficiary to withdraw all tokens
        if (
            block.timestamp >=
            linear_vesting_details[msg.sender].start + duration
        ) {
            token.transfer(
                linear_vesting_details[msg.sender].receiver,
                linear_vesting_details[msg.sender].totalAmount
            );
            linear_vesting_details[msg.sender].totalAmount = 0;
        } else {
            // calculate the percentage of time since the start of vesting
            uint256 timePercentage = (block.timestamp -
                linear_vesting_details[msg.sender].start) / duration;

            // how many tokens are available to be released based on the time elapsed since the start of vesting
            uint256 availableAmount = timePercentage *
                linear_vesting_details[msg.sender].amount;

            // Check if the totalAmount is greater than the availableAmount
            require(
                linear_vesting_details[msg.sender].totalAmount >=
                    availableAmount,
                "No tokens available for release"
            );

            // Update the total amount
            linear_vesting_details[msg.sender].totalAmount -= availableAmount;

            // Transfer these tokens to the beneficiary
            token.transfer(
                linear_vesting_details[msg.sender].receiver,
                availableAmount
            );
        }
    }
}

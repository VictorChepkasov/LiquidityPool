// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Ownable {
    address payable public owner;

    constructor() {
        owner = payable(msg.sender);
    }

    modifier onlyOwner() {
        require(owner == msg.sender, "Only owner!");
        _;
    }
}
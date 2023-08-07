// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./WETH.sol";

contract TestToken is ERC20 {
    using SafeERC20 for ERC20;

    constructor(address emiter) ERC20("Test MyToken", "TMT") {
        _mint(emiter, 10000);
    }
}

contract testTokenFactory {
    IERC20 public token;
    address payable public owner;

    constructor() {
        token = new TestToken(address(this));
        owner = payable(msg.sender);
    }

    function sell(uint _amountToSell) external {
        require(
            _amountToSell > 0 &&
            token.balanceOf(msg.sender) >= _amountToSell, 
            "Incorrect amount!"
        );

        uint allowance = token.allowance(msg.sender, address(this));
        require(allowance >= _amountToSell, "Check allowance!");

        token.transferFrom(msg.sender, address(this), _amountToSell);

        payable(msg.sender).transfer(_amountToSell);
    }

    function tokenBalance() public view returns(uint) {
        return token.balanceOf(address(this));
    }

    receive() external payable {
        uint tokensToBuy = msg.value; //1 wei == 1 token
        require(tokensToBuy > 0, "Not enough funds!");

        require(tokenBalance() >= tokensToBuy, "Not enough tokens!");

        token.transfer(msg.sender, tokensToBuy);
    }
}
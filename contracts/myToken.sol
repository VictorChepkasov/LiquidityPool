// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./WETH.sol";
import "./ownable.sol";

contract TestMyToken is ERC20 {
    using SafeERC20 for ERC20;

    constructor(address emiter) ERC20("Test MyToken", "TMT") {
        _mint(emiter, 10000);
    }
}

contract TestMyTokenFactory is Ownable {
    IERC20 public token;

    constructor() {
        token = new TestMyToken(address(this));
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
        return token.balanceOf(msg.sender);
    }

    receive() external payable {
        //1 wei == 1 token
        require(msg.value > 0, "Not enough funds!");

        require(tokenBalance() >= msg.value, "Not enough tokens!");

        token.transfer(msg.sender, msg.value);
    }
}
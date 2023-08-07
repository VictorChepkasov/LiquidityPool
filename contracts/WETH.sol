// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "./ownable.sol";

contract WrappedETH is ERC20 {
    using SafeERC20 for ERC20;

    constructor(address emiter) ERC20("Wrapped Ether", "WETH") {}

    function mint(address to, uint amount) public {
        _mint(to, amount);
    }

    function burn(address to, uint amount) public {
        _burn(to, amount);
    }
}

contract WETHFactory is Ownable {
    ERC20 public token;

    constructor() {
        token = new WETH(address(this));
    }

    function sell(uint _amountToSell) external {
        require(_amountToSell > 0 &&
        token.balanceOf(msg.sender) >= _amountToSell,
        "Incorrect amount!"
        );

        uint allowance = token.allowance(msg.sender, address(this));
        require(allowance >= _amountToSell, "Check allowance!");

        WETH(address(token)).burn(msg.sender, _amountToSell);

        payable(msg.sender).transfer(_amountToSell);
    }

    receive() external payable {
        uint tokenToBuy = msg.value; //1 eth == 1 token
        require(tokenToBuy > 0, "Not enough funds!");

        WETH(address(token)).mint(msg.sender, tokenToBuy);
    }
}
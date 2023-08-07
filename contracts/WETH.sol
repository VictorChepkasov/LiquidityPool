// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "./ownable.sol";

contract WETH is ERC20 {
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
    ERC20 public weth;

    constructor() {
        weth = new WETH(address(this));
    }

    function sell(uint _amountToSell) external {
        require(_amountToSell > 0 &&
        weth.balanceOf(msg.sender) >= _amountToSell,
        "Incorrect amount!"
        );

        uint allowance = weth.allowance(msg.sender, address(this));
        require(allowance >= _amountToSell, "Check allowance!");

        WETH(address(weth)).burn(msg.sender, _amountToSell);

        payable(msg.sender).transfer(_amountToSell);
    }

    receive() external payable {
        uint wethToBuy = msg.value; //1 eth == 1 weth
        require(wethToBuy > 0, "Not enough funds!");

        WETH(address(weth)).mint(msg.sender, wethToBuy);
    }
}
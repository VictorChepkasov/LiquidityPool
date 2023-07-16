// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract LiquidityPool {
    using SafeERC20 for ERC20;

    ERC20 public eth;
    //1inch - крутой агрегатор ликвидности
    ERC20 public inch;

    constructor(ERC20 _eth, ERC20 _inch) {
        eth = _eth;
        inch = _inch;
    }

    function createDeposit(ERC20 token, uint amount) public {
        bool txResult = token.transferFrom(msg.sender, address(this), amount);
        require(txResult, "Transfer failed!");
    }

    function withdraw(ERC20 token, uint amount) public {
        bool txResult = token.transfer(msg.sender, amount);
        require(txResult, "Transfer failed!");
    }

    function getExchangeRate() public view returns(uint) {
        uint ethBalance = eth.balanceOf(address(this));
        uint inchBalance = inch.balanceOf(address(this));
        return (inchBalance * 1 ether) / ethBalance;
    }

    function exchange(ERC20 fromToken, ERC20 toToken, uint fromAmount) public {
        require(fromToken == eth || fromToken == inch, "Invailid fromToken!");
        require(toToken == eth || toToken == inch, "Invailid toToken!");

        uint fromTokenBalance = fromToken.balanceOf(address(this));
        uint toTokenBalance = toToken.balanceOf(address(this));
        require(fromTokenBalance >= toTokenBalance, "You don't have money :(");

        uint exchangeRate = getExchangeRate();
        uint toAmount;
        if (fromToken == eth) {
            toAmount = (fromAmount * exchangeRate) / 1 ether;
        } else {
            toAmount = (fromAmount * 1 ether) / exchangeRate;
        }

        bool txFromTokenResult = fromToken.transferFrom(msg.sender, address(this), toAmount);
        require(txFromTokenResult, "Transfer failed!");
        bool txToTokenResult = toToken.transfer(msg.sender, toAmount);
        require(txToTokenResult, "Transfer failed!");
    }
}
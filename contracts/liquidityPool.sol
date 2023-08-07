// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./myToken.sol";

contract LiquidityPool {
    using SafeERC20 for ERC20;

    ERC20 public eth;
    ERC20 public myToken;

    constructor(ERC20 _eth, ERC20 _myToken) {
        eth = _eth;
        myToken = _myToken;
    }

    function createDeposit(ERC20 token, uint amount) public {
        bool txResult = token.transferFrom(msg.sender, address(this), amount);
        require(txResult, "Transfer failed!");
    }

    function withdraw(ERC20 token, uint amount) public {
        bool txResult = token.transfer(msg.sender, amount);
        require(txResult, "Transfer failed!");
    }

    function exchange(ERC20 fromToken, ERC20 toToken, uint fromAmount) public {
        require(
            fromToken == eth || fromToken == myToken, 
            "Invailid fromToken!"
        );
        require(
            toToken == eth || toToken == myToken,
            "Invailid toToken!"
        );

        uint fromTokenBalance = fromToken.balanceOf(address(this));
        uint toTokenBalance = toToken.balanceOf(address(this));
        require(
            fromTokenBalance >= toTokenBalance,
            "You don't have money :("
        );

        uint exchangeRate = getExchangeRate();
        uint toAmount = fromToken == eth ? (fromAmount * exchangeRate) / 1 ether : (fromAmount * 1 ether) / exchangeRate;

        bool txFromTokenResult = fromToken.transferFrom(msg.sender, address(this), toAmount);
        require(txFromTokenResult, "Transfer failed!");
        bool txToTokenResult = toToken.transfer(msg.sender, toAmount);
        require(txToTokenResult, "Transfer failed!");
    }
    
    function getExchangeRate() public view returns(uint) {
        uint ethBalance = eth.balanceOf(address(this));
        uint myTokenBalance = myToken.balanceOf(address(this));
        return (myTokenBalance * 1 ether) / ethBalance;
    }
}
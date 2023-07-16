// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
// import "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
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
}
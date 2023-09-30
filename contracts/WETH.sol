// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import '@openzeppelin/contracts/token/ERC20/ERC20.sol';
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract WrappedETH is ERC20 {
    using SafeERC20 for ERC20;

    constructor() ERC20('Wrapped Ether', 'WETH') {}

    function deposit() external payable {
        //1 eth == 1 weth
        require(msg.value > 0, "Not enough funds!");
        _mint(msg.sender, msg.value);
    }

    function withdraw(uint _amount) external {
        require(balanceOf(msg.sender) >= _amount, 'Incorrect amount');
        _burn(msg.sender, _amount);
        payable(msg.sender).transfer(_amount);
    }
}
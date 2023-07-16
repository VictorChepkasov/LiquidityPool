import pytest
from brownie import accounts
from scripts.deployLiquidityPool import deployLiquidityPool as deploy
from ..scripts.liquidityPoolScripts import (
    createDeposit,
    withdraw,
    exchange,
    getExchangeRate
)

@pytest.fixture()
def importAccounts():
    _from = accounts[0]
    eth = accounts[1]
    inch = accounts[2]
    contract = deploy(_from, eth, inch)
    return _from, eth, inch, contract

# def test_createDeposit():

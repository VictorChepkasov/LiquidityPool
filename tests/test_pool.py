import pytest
from brownie import accounts
from scripts.deployPool import deployLiquidityPool as deploy
from scripts.scriptsPool import (
    createDeposit,
    withdraw,
    exchange,
    getExchangeRate
)

@pytest.fixture()
def importAccounts():
    _from = accounts[0]
    eth = accounts[0]
    myToken = accounts[0]
    contract = deploy(_from, eth, myToken)
    return _from, eth, myToken, contract

def test_createDeposit(importAccounts, amount=100):
    _from, _eth, _myToken, _contract = importAccounts
    createDeposit(_from, _eth, amount)
    ethBalance = _eth.balanceOf(_contract)
    assert ethBalance == amount

# def test_exchangeRate(importAccounts, amount=100):
#     _from, _eth, _myToken, _contract = importAccounts
    
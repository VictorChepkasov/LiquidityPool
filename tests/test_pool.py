import pytest
from brownie import accounts, EtherTestToken
from test_token import depositMark
from scripts.deployToken import deployToken
from scripts.deployPool import deployLiquidityPool
from scripts.scriptsPool import (
    createDeposit,
    withdraw,
    exchange,
    getExchangeRate
)

@pytest.mark.parametrize('deposit', depositMark)
def test_deployPool(deposit):
    owner = accounts[0]
    myToken = deployToken(owner)
    owner.transfer(myToken.address, f'{deposit} wei', priority_fee='10 wei')

    deployed = deployLiquidityPool(owner, owner, myToken.token())

    assert str(deployed.address) != '0'

def test_createDeposit(deposit=100, amount=50):
    owner = accounts[0]
    myToken = deployToken(owner)
    owner.transfer(myToken.address, f'{deposit} wei', priority_fee='10 wei')
    deployed = deployLiquidityPool(owner, owner, myToken.token())
    testToken = EtherTestToken.at(myToken.token())
    ownerTokenBalance = testToken.balanceOf(owner)

    testToken.approve(deployed.address, amount, {
        'from': owner,
        'priority_fee': '1 wei'
    })
    createDeposit(owner, myToken.token(), amount)

    assert testToken.balanceOf(owner) == ownerTokenBalance - amount
    assert testToken.balanceOf(deployed.address) == amount
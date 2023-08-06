import pytest
from brownie import accounts, EtherTestToken
from test_token import depositMark, ownerAndFactory, testToken
# from scripts.deployToken import deployToken
from scripts.deployPool import deployLiquidityPool
from scripts.scriptsPool import (
    createDeposit,
    withdraw,
    exchange,
    getExchangeRate
)

@pytest.mark.parametrize('deposit', depositMark)
def test_deployPool(ownerAndFactory, deposit):
    owner, myToken = ownerAndFactory
    owner.transfer(myToken.address, f'{deposit} wei', priority_fee='10 wei')

    deployed = deployLiquidityPool(owner, owner, myToken.token())

    assert str(deployed.address) != '0'

@pytest.mark.parametrize(
        'deposit, amount',
        [pytest.param((0, 0), "Your don't have tokens :(", marks=pytest.mark.xfail), pytest.param((100, 120), "Transfer amount exceeds balance!", marks=pytest.mark.xfail), (100, 50)]
)
def test_createDeposit(ownerAndFactory, testToken, deposit, amount):
    owner, myToken = ownerAndFactory
    owner.transfer(myToken.address, f'{deposit} wei', priority_fee='10 wei')
    deployed = deployLiquidityPool(owner, owner, myToken.token())
    ownerTokenBalance = testToken.balanceOf(owner)

    testToken.approve(deployed.address, amount, {
        'from': owner,
        'priority_fee': '1 wei'
    })
    createDeposit(owner, myToken.token(), amount)

    assert testToken.balanceOf(owner) == ownerTokenBalance - amount
    assert testToken.balanceOf(deployed.address) == amount
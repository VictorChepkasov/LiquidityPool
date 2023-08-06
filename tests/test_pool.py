import pytest
from brownie import accounts, EtherTestToken
from test_token import amountToBuyMark, ownerAndFactory, testToken, buyTokens
from scripts.deployPool import deployLiquidityPool
from scripts.scriptsPool import (
    createDeposit,
    withdraw,
    exchange,
    getExchangeRate
)

@pytest.mark.parametrize('amountToBuy', amountToBuyMark)
def test_deployPool(ownerAndFactory, amountToBuy):
    owner, myToken = ownerAndFactory
    buyTokens(owner, myToken.address, amountToBuy)

    deployed = deployLiquidityPool(owner, owner, myToken.token())

    assert str(deployed.address) != '0'

@pytest.mark.parametrize(
        'amountToBuy, deposit',
        [pytest.param((0, 0), "Your don't have tokens :(", marks=pytest.mark.xfail), pytest.param((100, 120), "Transfer amount exceeds balance!", marks=pytest.mark.xfail), (100, 50)]
)
def test_createDeposit(ownerAndFactory, testToken, amountToBuy, deposit):
    owner, myToken = ownerAndFactory
    buyTokens(owner, myToken.address, amountToBuy)
    deployed = deployLiquidityPool(owner, owner, myToken.token())
    ownerTokenBalance = testToken.balanceOf(owner)

    testToken.approve(deployed.address, deposit, {
        'from': owner,
        'priority_fee': '1 wei'
    })
    createDeposit(owner, myToken.token(), deposit)

    assert testToken.balanceOf(owner) == ownerTokenBalance - deposit
    assert testToken.balanceOf(deployed.address) == deposit

# @pytest.mark.parametrize('deposit', depositMark)
# def test_withdraw(ownerAndFactory, testToken, deposit):
#     owner, myToken = ownerAndFactory

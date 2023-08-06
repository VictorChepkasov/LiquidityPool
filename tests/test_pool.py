import pytest
from test_token import amountToBuyMark, ownerAndFactory, testToken
from scripts.deployPool import deployLiquidityPool
from scripts.scriptsPool import (
    createDeposit,
    withdraw,
    exchange,
    getExchangeRate,
    buyTokens,
    approve
)

@pytest.mark.parametrize('amountToBuy', amountToBuyMark)
def test_deployPool(ownerAndFactory, amountToBuy):
    owner, myToken = ownerAndFactory
    buyTokens(owner, myToken.address, amountToBuy)
    pool = deployLiquidityPool(owner, owner, myToken.token())

    assert str(pool.address) != '0'

@pytest.mark.parametrize(
        'amountToBuy, deposit',
        [pytest.param((0, 0), "Your don't have tokens :(", marks=pytest.mark.xfail), pytest.param((100, 120), "Transfer amount exceeds balance!", marks=pytest.mark.xfail), (100, 50)]
)
def test_createDeposit(ownerAndFactory, testToken, amountToBuy, deposit):
    owner, myToken = ownerAndFactory
    buyTokens(owner, myToken.address, amountToBuy)
    pool = deployLiquidityPool(owner, owner, myToken.token())
    ownerTokenBalance = testToken.balanceOf(owner)
    poolBalance = testToken.balanceOf(pool.address)

    approve(testToken, pool.address, deposit, owner)
    createDeposit(owner, myToken.token(), deposit)

    assert testToken.balanceOf(owner) == ownerTokenBalance - deposit
    assert testToken.balanceOf(pool.address) == poolBalance + deposit

# @pytest.mark.parametrize('deposit', amountToBuyMark)
# def test_withdraw(ownerAndFactory, testToken, deposit):
#     owner, myToken = ownerAndFactory
#     buyTokens(owner, myToken.address, deposit)
#     pool = deployLiquidityPool(owner, owner, myToken.token())
#     poolBalance = testToken.balanceOf(pool.address)
#     ownerTokenBalance = testToken.balanceOf(owner)
    
#     approve(testToken, pool.address, deposit, owner)
#     createDeposit(owner, myToken.token(), deposit)
#     withdraw(owner, myToken.address, deposit)

#     assert testToken.balanceOf(owner) == ownerTokenBalance + deposit
#     assert testToken.balanceOf(pool.address) == poolBalance - deposit
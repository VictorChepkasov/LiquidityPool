import pytest
from brownie import accounts
from scripts.deployPool import deployLiquidityPool
from scripts.scriptsPool import (
    createDeposit,
    withdraw,
    exchange,
    getExchangeRate,
    buyTokens,
    approve
)
from test_token import (
    amountToBuyMark,
    ownerAndFactories,
    testToken,
    wethToken
)

@pytest.mark.parametrize('amountToBuy', amountToBuyMark)
def test_deployPool(ownerAndFactories, amountToBuy):
    owner, myToken, weth = ownerAndFactories
    buyTokens(owner, myToken.address, amountToBuy)
    pool = deployLiquidityPool(owner, weth.token(), myToken.token())

    assert str(pool.address) != '0'

@pytest.mark.parametrize(
        'amountToBuy, deposit',
        [pytest.param((0, 0), "Your don't have tokens :(", marks=pytest.mark.xfail), pytest.param((100, 120), "Transfer amount exceeds balance!", marks=pytest.mark.xfail), (100, 50)]
)
def test_createDeposit(ownerAndFactories, testToken, amountToBuy, deposit):
    owner, myToken, weth = ownerAndFactories
    buyTokens(owner, myToken.address, amountToBuy)
    pool = deployLiquidityPool(owner, weth.token(), myToken.token())
    ownerTokenBalance = testToken.balanceOf(owner)
    poolBalance = testToken.balanceOf(pool.address)

    approve(testToken, pool.address, deposit, owner)
    createDeposit(owner, myToken.token(), deposit)

    assert testToken.balanceOf(owner) == ownerTokenBalance - deposit
    assert testToken.balanceOf(pool.address) == poolBalance + deposit

@pytest.mark.parametrize('deposit', amountToBuyMark)
def test_withdraw(ownerAndFactories, testToken, deposit):
    owner, myToken, weth = ownerAndFactories
    buyTokens(owner, myToken.address, deposit)
    pool = deployLiquidityPool(owner, weth.token(), myToken.token())
    approve(testToken, pool.address, deposit, owner)
    createDeposit(owner, myToken.token(), deposit)

    ownerTokenBalance = testToken.balanceOf(owner)
    poolBalance = testToken.balanceOf(pool.address)
    withdraw(owner, myToken.token(), deposit)

    assert testToken.balanceOf(owner) == ownerTokenBalance + deposit
    assert testToken.balanceOf(pool.address) == poolBalance - deposit

@pytest.mark.parametrize('deposit', amountToBuyMark)
def test_exchange(ownerAndFactories, testToken, wethToken, deposit, amount=10):
    owner, myToken, weth = ownerAndFactories
    buyTokens(owner, myToken.address, deposit*2)
    print(f'MyToken balance: {testToken.balanceOf(owner.address)}')
    pool = deployLiquidityPool(owner, weth.token(), myToken.token())

    approve(testToken, pool.address, deposit, owner)
    createDeposit(owner, myToken.token(), deposit)

    buyTokens(owner, weth.address, deposit*2)
    print(f'WETH Balance: {wethToken.balanceOf(owner.address)}')

    buyTokens(accounts[2], weth.address, deposit*2)
    approve(wethToken, pool.address, deposit*2, accounts[2])
    createDeposit(accounts[2], weth.token(), deposit)

    approve(testToken, pool.address, amount, owner)
    print(f'Pool TMT balance: {testToken.balanceOf(pool.address)}')
    print(f'Pool WETH balance: {wethToken.balanceOf(pool.address)}')
    exchange(owner, testToken, wethToken, amount)
    
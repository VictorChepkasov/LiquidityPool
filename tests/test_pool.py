import pytest
from brownie import accounts, TestMyToken, WrappedETH
from scripts.deployMyToken import deployToken
from scripts.deployWETH import deployWETH
from scripts.deployPool import deployLiquidityPool
from scripts.scriptsPool import (
    createDeposit,
    withdraw,
    exchange,
    getExchangeRate,
    buyTokens,
    approve
)

amountToBuyMark = [pytest.param(0, marks=pytest.mark.xfail), 10, pytest.param(100000, marks=pytest.mark.xfail)]

@pytest.fixture(params=['TMT', 'WETH'])
def tokenAndFactory(request):
    owner = accounts[0]
    if request.param == 'TMT':
        tokenFactory = deployToken(owner)
        token = TestMyToken.at(tokenFactory.token())
    else:
        tokenFactory = deployWETH(owner)
        token = WrappedETH.at(tokenFactory.token())
    return owner, tokenFactory, token, request.param

@pytest.fixture(params=amountToBuyMark)
def pool(request):
    owner = accounts[0]
    tmtFactory = deployToken(owner)
    tmt = TestMyToken.at(tmtFactory.token())
    wethFactory = deployWETH(owner)
    weth = WrappedETH.at(wethFactory.token())
    buyTokens(owner, tmtFactory.address, request.param)

    return deployLiquidityPool(owner, wethFactory.token(), tmtFactory.token())

@pytest.mark.parametrize('amountToBuy', amountToBuyMark)
def test_deployPool(amountToBuy):
    owner = accounts[0]
    tmtFactory = deployToken(owner)
    wethFactory = deployWETH(owner)

    buyTokens(owner, tmtFactory.address, amountToBuy)
    pool = deployLiquidityPool(owner, wethFactory.token(), tmtFactory.token())

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

# @pytest.mark.parametrize('deposit', amountToBuyMark)
# def test_withdraw(ownerAndFactories, testToken, deposit):
#     owner, myToken, weth = ownerAndFactories
#     buyTokens(owner, myToken.address, deposit)
#     pool = deployLiquidityPool(owner, weth.token(), myToken.token())
#     approve(testToken, pool.address, deposit, owner)
#     createDeposit(owner, myToken.token(), deposit)

#     ownerTokenBalance = testToken.balanceOf(owner)
#     poolBalance = testToken.balanceOf(pool.address)
#     withdraw(owner, myToken.token(), deposit)

#     assert testToken.balanceOf(owner) == ownerTokenBalance + deposit
#     assert testToken.balanceOf(pool.address) == poolBalance - deposit

# @pytest.mark.parametrize('deposit', amountToBuyMark)
# def test_exchange(ownerAndFactories, testToken, wethToken, deposit, amount=10):
#     owner, myToken, weth = ownerAndFactories
#     buyTokens(owner, myToken.address, deposit*2)
#     print(f'MyToken balance: {testToken.balanceOf(owner.address)}')
#     pool = deployLiquidityPool(owner, weth.token(), myToken.token())

#     approve(testToken, pool.address, deposit, owner)
#     createDeposit(owner, myToken.token(), deposit)

#     buyTokens(owner, weth.address, deposit*2)
#     print(f'WETH Balance: {wethToken.balanceOf(owner.address)}')

#     buyTokens(accounts[2], weth.address, deposit*2)
#     approve(wethToken, pool.address, deposit*2, accounts[2])
#     createDeposit(accounts[2], weth.token(), deposit)

#     approve(testToken, pool.address, amount, owner)
#     print(f'Pool TMT balance: {testToken.balanceOf(pool.address)}')
#     print(f'Pool WETH balance: {wethToken.balanceOf(pool.address)}')
#     exchange(owner, testToken, wethToken, amount)
    
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
def pool(request, tokenAndFactory):
    owner, tokenFactory, _, _ = tokenAndFactory
    tmtFactory = deployToken(owner)
    wethFactory = deployWETH(owner)
    buyTokens(owner, tokenFactory.address, request.param)

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
def test_createDeposit(tokenAndFactory, amountToBuy, deposit):
    owner, tokenFactory, token, requestParam = tokenAndFactory
    buyTokens(owner, tokenFactory.address, amountToBuy)
    if requestParam == 'TMT':
        tmtFactory, wethFactory = tokenFactory, deployWETH(owner)
    else:
        tmtFactory, wethFactory = deployToken(owner), tokenFactory
    pool = deployLiquidityPool(owner, wethFactory.token(), tmtFactory.token())

    ownerTokenBalance = token.balanceOf(owner)
    poolBalance = token.balanceOf(pool.address)

    approve(token, pool.address, deposit, owner)
    createDeposit(owner, tokenFactory.token(), deposit)

    assert token.balanceOf(owner) == ownerTokenBalance - deposit
    assert token.balanceOf(pool.address) == poolBalance + deposit

# депозит равен 10, задача теста вывести его на счёт вкладчика
def test_withdraw(tokenAndFactory, deposit=10):
    owner, tokenFactory, token, requestParam = tokenAndFactory
    buyTokens(owner, tokenFactory.address, deposit)
    if requestParam == 'TMT':
        tmtFactory, wethFactory = tokenFactory, deployWETH(owner)
    else:
        tmtFactory, wethFactory = deployToken(owner), tokenFactory
    pool = deployLiquidityPool(owner, wethFactory.token(), tmtFactory.token())

    approve(token, pool.address, deposit, owner)
    createDeposit(owner, tokenFactory.token(), deposit)

    ownerTokenBalance = token.balanceOf(owner)
    poolBalance = token.balanceOf(pool.address)
    withdraw(owner, tokenFactory.token(), deposit)

    assert token.balanceOf(owner) == ownerTokenBalance + deposit
    assert token.balanceOf(pool.address) == poolBalance - deposit

@pytest.mark.parametrize('deposit', amountToBuyMark)
def test_exchange(tokenAndFactory, deposit, amount=10):
    owner, _, _, requestParam = tokenAndFactory
    if requestParam == 'TMT':
        _, toTokenFactory, toToken, _ = tokenAndFactory
        fromTokenFactory = deployWETH(owner)
        fromToken = WrappedETH.at(fromTokenFactory.token())
    else:
        _, toTokenFactory, toToken, _ = tokenAndFactory
        fromTokenFactory = deployToken(owner)
        fromToken = TestMyToken.at(fromTokenFactory.token())

    buyTokens(owner, toTokenFactory.address, deposit*2)
    pool = deployLiquidityPool(owner, fromTokenFactory.token(), toTokenFactory.token())

    approve(toToken, pool.address, deposit, owner)
    createDeposit(owner, toTokenFactory.token(), deposit)

    buyTokens(owner, fromTokenFactory.address, deposit*2)
    print(f'WETH Balance: {fromToken.balanceOf(owner.address)}')

    buyTokens(accounts[2], fromTokenFactory.address, deposit*2)
    approve(fromToken, pool.address, deposit*2, accounts[2])
    createDeposit(accounts[2], fromTokenFactory.token(), deposit)

    approve(toToken, pool.address, amount, owner)
    print(f'Pool TMT balance: {toToken.balanceOf(pool.address)}')
    print(f'Pool WETH balance: {fromToken.balanceOf(pool.address)}')
    exchange(owner, toToken, fromToken, amount)
    
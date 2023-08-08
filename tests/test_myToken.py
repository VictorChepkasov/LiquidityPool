import pytest
from brownie import accounts, TestMyToken, WrappedETH
from scripts.scriptsPool import buyTokens, approve
from scripts.deployMyToken import deployToken
from scripts.deployWETH import deployWETH

'''
tmt - контракт фабрики токена Test My Token (TMT)
weth - контракт фабрики токена weth
tmtToken - контракт самого токена 
wethToken - контракт самого токена
'''

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

@pytest.mark.parametrize('amountToBuy', [pytest.param(0, marks=pytest.mark.xfail), 10, pytest.param(100000, marks=pytest.mark.xfail)])
def test_buyingToken(amountToBuy, tokenAndFactory):
    owner, tokenFactory, token, request = tokenAndFactory
    ownerBalance = owner.balance()

    tokenBalance = tokenFactory.tokenBalance()
    ownerTokenBalance = token.balanceOf(owner)
    buyTokens(owner, tokenFactory.address, amountToBuy)
    newTokenBalance = tokenFactory.tokenBalance() + amountToBuy if request == 'TMT' else 0

    # xpassed при WETH-100000, т.к. weth выпускает и сжигает токены, но не хранит их
    assert tokenBalance == newTokenBalance
    assert ownerTokenBalance == token.balanceOf(owner) - amountToBuy
    assert owner.balance() <= ownerBalance

@pytest.mark.parametrize('amountToSell', [pytest.param(0, marks=pytest.mark.xfail), 5])
def test_sellingToken(tokenAndFactory, amountToSell):
    owner, tokenFactory, token, request = tokenAndFactory
    buyTokens(owner, tokenFactory.address, 20)
    ownerTokenBalance = token.balanceOf(owner)
    tokenBalance = tokenFactory.tokenBalance()
    
    approve(token, tokenFactory.address, amountToSell, owner)
    tokenFactory.sell(amountToSell, {'priority_fee': '1 wei'})
    newTokenBalance = tokenBalance  if request == 'WETH' else tokenBalance + amountToSell
    
    assert tokenFactory.tokenBalance() == newTokenBalance
    assert token.balanceOf(owner) == ownerTokenBalance - amountToSell


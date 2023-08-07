import pytest
from brownie import accounts, TestToken, WrappedETH
from scripts.scriptsPool import buyTokens, approve
from scripts.deployToken import deployToken
from scripts.deployWETH import deployWETH

amountToBuyMark = [pytest.param(0, marks=pytest.mark.xfail), 10, 1000, pytest.param(100000, marks=pytest.mark.xfail)]

@pytest.fixture()
def ownerAndFactories():
    owner = accounts[0]
    return owner, deployToken(owner), deployWETH(owner)

@pytest.fixture()
def testToken(ownerAndFactories):
    _, myToken, _ = ownerAndFactories
    return TestToken.at(myToken.token())

@pytest.fixture()
def wethToken(ownerAndFactories):
    _, _, weth = ownerAndFactories
    return WrappedETH.at(weth.token())

@pytest.mark.parametrize('amountToBuy', amountToBuyMark)
def test_buyingToken(ownerAndFactories, testToken, amountToBuy):
    owner, myToken = ownerAndFactories
    ownerBalance = owner.balance()

    buyTokens(owner, myToken.address, amountToBuy)
    tokenBalance = myToken.tokenBalance()
    ownerTokenBalance = testToken.balanceOf(owner)

    assert tokenBalance == 10000 - amountToBuy
    assert ownerTokenBalance == amountToBuy
    assert owner.balance() <= ownerBalance

@pytest.mark.parametrize('amountToBuy', amountToBuyMark)
def test_sellingToken(ownerAndFactories, testToken, amountToBuy, amountToSell=9):
    owner, myToken = ownerAndFactories
    buyTokens(owner, myToken.address, amountToBuy)
    
    approve(testToken, myToken.address, amountToSell, owner)
    ownerTokenBalance = testToken.balanceOf(owner)
    tokenBalance = myToken.tokenBalance()
    myToken.sell(amountToSell, {'priority_fee': '1 wei'})
    
    assert myToken.tokenBalance() == tokenBalance + amountToSell
    assert testToken.balanceOf(owner) == ownerTokenBalance - amountToSell


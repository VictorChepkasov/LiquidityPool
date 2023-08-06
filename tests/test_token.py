import pytest
from brownie import accounts, EtherTestToken
from scripts.deployToken import deployToken

amountToBuyMark = [pytest.param(0, marks=pytest.mark.xfail), 10, 1000, pytest.param(100000, marks=pytest.mark.xfail)]

@pytest.fixture()
def ownerAndFactory():
    owner = accounts[0]
    return owner, deployToken(owner)

@pytest.fixture()
def testToken(ownerAndFactory):
    _, myToken = ownerAndFactory
    return EtherTestToken.at(myToken.token())

def buyTokens(_from, _tokenAddress, _amountToBuy):
    _from.transfer(_tokenAddress, f'{_amountToBuy} wei', priority_fee='10 wei')

@pytest.mark.parametrize('amountToBuy', amountToBuyMark)
def test_buyingToken(ownerAndFactory, testToken, amountToBuy):
    owner, myToken = ownerAndFactory
    ownerBalance = owner.balance()

    buyTokens(owner, myToken.address, amountToBuy)
    tokenBalance = myToken.tokenBalance()
    ownerTokenBalance = testToken.balanceOf(owner)

    assert tokenBalance == 10000 - amountToBuy
    assert ownerTokenBalance == amountToBuy
    assert owner.balance() <= ownerBalance

@pytest.mark.parametrize('amountToBuy', amountToBuyMark)
def test_sellingToken(ownerAndFactory, testToken, amountToBuy, amountToSell=9):
    owner, myToken = ownerAndFactory
    buyTokens(owner, myToken.address, amountToBuy)
    
    testToken.approve(myToken.address, amountToSell, {
        'from': owner,
        'priority_fee': '1 wei'
    })
    ownerTokenBalance = testToken.balanceOf(owner)
    tokenBalance = myToken.tokenBalance()
    myToken.sell(amountToSell, {'priority_fee': '1 wei'})
    
    assert myToken.tokenBalance() == tokenBalance + amountToSell
    assert testToken.balanceOf(owner) == ownerTokenBalance - amountToSell


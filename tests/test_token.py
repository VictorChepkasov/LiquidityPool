import pytest
from brownie import accounts, EtherTestToken
from scripts.deployToken import deployToken

depositMark = [pytest.param(0, marks=pytest.mark.xfail), 10, 1000, pytest.param(100000, marks=pytest.mark.xfail)]

@pytest.fixture()
def ownerAndFactory():
    owner = accounts[0]
    return owner, deployToken(owner)

@pytest.fixture()
def testToken(ownerAndFactory):
    _, myToken = ownerAndFactory
    return EtherTestToken.at(myToken.token())

@pytest.mark.parametrize('amountToBuy', depositMark)
def test_buyingToken(ownerAndFactory, testToken, amountToBuy):
    owner, myToken = ownerAndFactory
    ownerBalance = owner.balance()

    owner.transfer(myToken.address, f'{amountToBuy} wei', priority_fee='10 wei')
    tokenBalance = myToken.tokenBalance()
    ownerTokenBalance = testToken.balanceOf(owner)

    assert tokenBalance == 10000 - amountToBuy
    assert ownerTokenBalance == amountToBuy
    assert owner.balance() <= ownerBalance

@pytest.mark.parametrize('deposit', depositMark)
def test_sellingToken(ownerAndFactory, testToken, deposit, amountToSell=9):
    owner, myToken = ownerAndFactory
    owner.transfer(myToken.address, f'{deposit} wei', priority_fee='1 wei')
    
    testToken.approve(myToken.address, amountToSell, {
        'from': owner,
        'priority_fee': '1 wei'
    })
    ownerTokenBalance = testToken.balanceOf(owner)
    tokenBalance = myToken.tokenBalance()
    myToken.sell(amountToSell, {'priority_fee': '1 wei'})
    
    assert myToken.tokenBalance() == tokenBalance + amountToSell
    assert testToken.balanceOf(owner) == ownerTokenBalance - amountToSell


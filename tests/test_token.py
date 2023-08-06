import pytest
from brownie import accounts, EtherTestToken
from scripts.deployToken import deployToken

depositMark = [pytest.param(0, marks=pytest.mark.xfail), 10, 1000, pytest.param(100000, marks=pytest.mark.xfail)]

@pytest.mark.parametrize('deposit', depositMark)
def test_buyingToken(deposit):
    owner = accounts[0]
    ownerBalance = owner.balance()
    myToken = deployToken(owner)

    owner.transfer(myToken.address, f'{deposit} wei', priority_fee='10 wei')
    etherTestToken = EtherTestToken.at(myToken.token())
    tokenBalance = myToken.tokenBalance()
    ownerTokenBalance = etherTestToken.balanceOf(owner)

    assert tokenBalance == 10000 - deposit
    assert ownerTokenBalance == deposit
    assert owner.balance() <= ownerBalance

@pytest.mark.parametrize('deposit', depositMark)
def test_sellingToken(deposit, amountToSell=9):
    owner = accounts[0]
    myToken = deployToken(owner)
    testToken = EtherTestToken.at(myToken.token())
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


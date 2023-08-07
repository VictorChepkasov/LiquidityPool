import pytest
from brownie import accounts, WrappedETH, WETHFactory
from scripts.scriptsPool import buyTokens, approve
from scripts.deployWETH import deployWETH

amountMark = [pytest.param(0, marks=pytest.mark.xfail), 10]

@pytest.fixture(autouse=True)
def env():
    owner = accounts[1]
    weth = deployWETH(owner)
    return owner, weth, WrappedETH.at(weth.token())

@pytest.mark.parametrize('amount', amountMark)
def test_minting(env, amount):
    owner, weth, wethToken = env
    ownerBalnace = wethToken.balanceOf(owner)
    totalSupply = wethToken.totalSupply()
    buyTokens(owner, weth.address, amount)
    assert ownerBalnace + amount == wethToken.balanceOf(owner)
    assert totalSupply + amount == wethToken.totalSupply() 

@pytest.mark.parametrize('amount', amountMark)
def test_burning(env, amount):
    owner, weth, wethToken = env
    buyTokens(owner, weth.address, amount)
    ownerBalance = wethToken.balanceOf(owner)
    totalSupply = wethToken.totalSupply()

    approve(wethToken, weth.address, amount, owner)
    WETHFactory[-1].sell(amount, {
        'from': owner,
        'priority_fee': '10 wei'
    })
    
    assert ownerBalance - amount == wethToken.balanceOf(owner) 
    assert totalSupply - amount == wethToken.totalSupply() 
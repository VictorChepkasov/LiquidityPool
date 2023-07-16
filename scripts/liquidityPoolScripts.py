from brownie import accounts, LiquidityPool
from scripts.deployLiquidityPool import deployLiquidityPool as deploy

def createDeposit(_from, _token, _amount):
    LiquidityPool[-1].createDeposit(_token, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print('Transfer successful!')

def withdraw(_from, _token, _amount):
    LiquidityPool[-1].withdraw(_token, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print('Transfer successful!')

def exchange(_fromToken, _toToken, _fromAmount):
    LiquidityPool[-1].exchange(_fromToken, _toToken, _fromAmount, {
        'from': _fromToken,
        'priority_fee': '10 wei'
    })

def getExchangeRate(_from):
    exchangeRate = LiquidityPool[-1].getExchangeRate({
        'from': _from,
        'priority_fee': '10 wei'
    })
    return exchangeRate
from brownie import LiquidityPool

def createDeposit(_from, _token, _amount):
    LiquidityPool[-1].createDeposit(_token, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print('Deposit created successfully!')

def withdraw(_from, _token, _amount):
    LiquidityPool[-1].withdraw(_token, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print('Transfer successful!')

def exchange(_from, _fromToken, _toToken, _fromAmount):
    LiquidityPool[-1].exchange(_fromToken, _toToken, _fromAmount, {
        'from': _from,
        'priority_fee': '10 wei',

    })

def getExchangeRate(_from):
    exchangeRate = LiquidityPool[-1].getExchangeRate({
        'from': _from,
        'priority_fee': '10 wei'
    })
    return exchangeRate

def buyTokens(_from, _tokenAddress, _amountToBuy):
    _from.transfer(_tokenAddress, f'{_amountToBuy} wei', priority_fee='10 wei')

def approve(_token, _spenderAddress, _amount, _from):
    _token.approve(_spenderAddress, _amount, {
        'from': _from,
        'priority_fee': '1 wei'
    })
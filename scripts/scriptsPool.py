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


# myToken = deployToken(accounts[0])
#     owner.transfer(myToken.address, '100 wei', priority_fee='1 wei')
#     etherTestToken = EtherTestToken.at(myToken.token())
#     print(f'Token balance: {myToken.tokenBalance()}')
#     print(f'Owner balance: {etherTestToken.balanceOf(owner)}')
#     deployLiquidityPool(owner, owner, myToken.token())
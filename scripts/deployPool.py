from brownie import accounts, LiquidityPool, EtherTestToken
from dotenv import load_dotenv
from scripts.deployToken import deployToken
from scripts.scriptsPool import createDeposit

load_dotenv()

def main():
    owner = accounts[0]
    myToken = deployToken(owner)
    owner.transfer(myToken.address, '100 wei', priority_fee='1 wei')
    print('Transaction successful!')
    etherTestToken = EtherTestToken.at(myToken.token())
    print(f'Token balance: {myToken.tokenBalance()}')
    print(f'Owner balance: {etherTestToken.balanceOf(owner)}')
    deployLiquidityPool(owner, owner, myToken.token())
    # createDeposit(owner, myToken.token(), 20)


def deployLiquidityPool(_from, _eth, _myToken):
    deployed = LiquidityPool.deploy(_eth, _myToken, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Contract deployed at: {deployed}')
    return deployed
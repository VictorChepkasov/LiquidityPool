from brownie import accounts, LiquidityPool
from dotenv import load_dotenv

load_dotenv()

def deployLiquidityPool(_from, _eth, _inch):
    deployed = LiquidityPool.deploy(_eth, _inch, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Contract deployed at: {deployed}')
    return deployed
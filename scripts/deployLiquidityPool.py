from brownie import accounts, LiquidityPool
from dotenv import load_dotenv

load_dotenv()

def main():
    acc = accounts[0]
    deployLiquidityPool(acc)

def deployLiquidityPool(_from):
    deployed = LiquidityPool.deploy(_from, _from, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Contract deployed at: {deployed}')
    return deployed
from brownie import accounts, LiquidityPool
from dotenv import load_dotenv

load_dotenv()

# def main():
#     deployLiquidityPool(accounts[0], accounts[0], accounts[0])

def deployLiquidityPool(_from, _eth, _myToken):
    deployed = LiquidityPool.deploy(_eth, _myToken, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Contract deployed at: {deployed}')
    # print(f'ABI: {deployed.abi}')
    return deployed
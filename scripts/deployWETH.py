from brownie import accounts, WETHFactory

def main():
    deployWETH(accounts[0])

def deployWETH(_from):
    deployed = WETHFactory.deploy({
        'from': _from,
        'priority_fee': '1 wei'
    })
    print(f'WETH Factory deployed at: {deployed}')
    return deployed
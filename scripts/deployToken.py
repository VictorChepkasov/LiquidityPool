from brownie import accounts, testTokenFactory
from dotenv import load_dotenv

def main():
    deployToken(accounts[0])

def deployToken(_from):
    deployed = testTokenFactory.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'MyToken factory deployed at: {deployed}\n')
    return deployed
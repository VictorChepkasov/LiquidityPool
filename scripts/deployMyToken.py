from brownie import accounts, TestMyTokenFactory
from dotenv import load_dotenv

def main():
    deployToken(accounts[0])

def deployToken(_from):
    deployed = TestMyTokenFactory.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'MyToken factory deployed at: {deployed}\n')
    return deployed
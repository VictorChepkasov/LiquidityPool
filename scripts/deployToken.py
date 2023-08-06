from brownie import accounts, EtherTestEmiter
from dotenv import load_dotenv

def main():
    deployToken(accounts[0])

def deployToken(_from):
    deployed = EtherTestEmiter.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Factory deployed at: {deployed}\n')
    return deployed
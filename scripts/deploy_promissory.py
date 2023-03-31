from brownie import Promissory, accounts
# from scripts.createjson import createMetadata
from dotenv import load_dotenv

load_dotenv()

holder = accounts.load("victor")

def deploy_contract():
    promissory_deploy_contract = Promissory.deploy({'from': holder, 'priority_fee': '1 wei'})
    print(f'contract deployed at {promissory_deploy_contract}')
    
    return promissory_deploy_contract

def main():
    deploy_contract()
    print('Deployed success!')
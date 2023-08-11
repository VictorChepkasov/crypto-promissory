from brownie import Promissory, accounts, config
from dotenv import load_dotenv

load_dotenv()

def main():
    holder = accounts.add(config["wallets"]["from_key"])
    deploy_promissory(holder)
    get_promissory_info(holder)

def deploy_promissory(_from, _debtor, _promissoryCommission, _promissoryAmount, _dateOfClose):
    promissoryContract = Promissory.deploy(_debtor, _promissoryCommission, _promissoryAmount, _dateOfClose, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Promissory deployed at {promissoryContract}')
    return promissoryContract

def get_promissory_info(_from):
    promissory_info = Promissory[-1].getPromissoryInfo({
        'from': _from
    })
    print(f'Promissory info: {promissory_info}')
    return promissory_info
from brownie import Promissory, accounts
from dotenv import load_dotenv
load_dotenv()

def main():
    holder = accounts.load('victor')
    debtor = accounts.load('victor2')
    deploy_promissory(holder, debtor, 10, 200000, 1692126000)

def deploy_promissory(_id, _from, _debtor, _promissory_commission, _promissory_amount, _date_of_close):
    promissory_deployed = Promissory.deploy(_id, _from, _debtor, _promissory_commission, _promissory_amount, _date_of_close, {
        'from': _from,
        'priority_fee': '2 gwei'
    })
    print(f'Promissory deployed at {promissory_deployed}')
    return promissory_deployed

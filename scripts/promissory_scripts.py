from brownie import Promissory, accounts, config
from dotenv import load_dotenv

load_dotenv()

def main():
    # holder = accounts.add(config["wallets"]["from_key"])
    holder = accounts.load('victor')
    debtor = accounts.load('victor2')
    deploy_promissory(holder, debtor, 10, 2000, 1692126000)
    # get_promissory_info(holder)
    set_debtor_consent(debtor)
    set_holder_consent(holder)
    pay_promissory(debtor)

def deploy_promissory(_from, _debtor, _promissoryCommission, _promissoryAmount, _dateOfClose):
    promissoryContract = Promissory.deploy(_debtor, _promissoryCommission, _promissoryAmount, _dateOfClose, {
        'from': _from,
        'priority_fee': '2 gwei'
    })
    print(f'Promissory deployed at {promissoryContract}')
    return promissoryContract

def get_promissory_info(_from):
    promissory_info = Promissory[-1].getPromissoryInfo({
        'from': _from
    })
    print(f'Promissory info: {promissory_info}')
    return promissory_info

def set_holder_consent(_from):
    Promissory[-1].setHolderConsent({
        'from': _from,
        'priority_fee': '0.2 gwei'
    })
    print('Holder consent saved!')

def set_debtor_consent(_from):
    Promissory[-1].setDebtorConsent({
        'from':_from,
        'priority_fee': '0.2 gwei'
    })
    print('Debtor consent saved!')

def pay_promissory(_from):
    Promissory[-1].payPromissory({
        'from': _from,
        'value': get_promissory_info(_from)[3],
        'priority_fee': '2 gwei'
    })
    print('Promissory was paid!')
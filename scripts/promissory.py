from brownie import Promissory, accounts
from dotenv import load_dotenv
load_dotenv()

def main():
    holder = accounts.load('victor')
    debtor = accounts.load('victor2')
    deploy_promissory(holder, debtor, 10, 200000, 1692126000)
    set_debtor_consent(debtor)
    set_holder_consent(holder)
    pay_promissory(debtor)

def deploy_promissory(_id, _from, _debtor, _promissory_commission, _promissory_amount, _date_of_close):
    promissory_deployed = Promissory.deploy(_id, _from, _debtor, _promissory_commission, _promissory_amount, _date_of_close, {
        'from': _from,
        'priority_fee': '2 gwei'
    })
    print(f'Promissory deployed at {promissory_deployed}')
    return promissory_deployed

# получение соглашения от векселедержателя
def set_holder_consent(_from):
    Promissory[-1].setHolderConsent({
        'from': _from,
        'priority_fee': '0.2 gwei'
    })
    print('Holder consent saved!')

# получение соглашения от векселедателя
def set_debtor_consent(_from):
    Promissory[-1].setDebtorConsent({
        'from':_from,
        'priority_fee': '0.2 gwei'
    })
    print('Debtor consent saved!')

# оплата векселя
def pay_promissory(_from):
    Promissory[-1].payPromissory({
        'from': _from,
        'value': get_promissory_info(_from)[4],
        'priority_fee': '2 gwei'
    })
    print('Promissory was paid!')

# получение структуры с информацией о векселе через контаркт векселя
def get_promissory_info(_from):
    promissory_info = Promissory[-1].getPromissoryInfo({
        'from': _from
    })
    print(f'Promissory info: {promissory_info}')
    return promissory_info
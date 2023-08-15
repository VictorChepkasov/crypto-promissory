from brownie import PromissoryNFT, Promissory, accounts, config
from scripts.metadata import create_metadata

def main():
    holder = accounts.load('victor')
    # deploy_promissory_nft(holder)
    create_promissory(holder, accounts.add(config['wallets']['debtor_key']), 0, 1000, 1691694000)

def deploy_promissory_nft(_from):
    promissory_nft_deployed = PromissoryNFT.deploy({
        "from": _from,
        'priority_fee': '2 gwei'
    })
    print(f"Promissory NFT deployed at {promissory_nft_deployed}")
    return promissory_nft_deployed

# Получение адреса контракта векселя по id, 
def get_promissory(_from, promissory_id):
    info = PromissoryNFT[-1].getPromissory(promissory_id, {
        'from': _from
    })
    return Promissory.at(info)

# Создание контракта, метаданных и выпуск токена
def create_promissory(_from, _debtor, _promissory_commission, _promissory_amount, _date_of_close):
    promissory_nft = PromissoryNFT[-1] 
    # проверяем количество отчеканенных на данный момент токенов
    existing_tokens = promissory_nft.tokenCounter()
    print(f'Existing tokens: {existing_tokens}')

    # вызываем нашу функцию createCollectible, чтобы создать контракт векселя 
    promissory_nft.createCollectible(_debtor, _promissory_commission, _promissory_amount, _date_of_close, {
        'from': _from,
        'priority_fee': '10 wei'
        # "gas_limit": 2074045
    })
    print('Create collectible!')

    # получаем хэш метаданных для URI этого токена
    metadata_uri = create_metadata(_from, existing_tokens+1)

    # выпускаем токен
    promissory_nft.mintCollectible(metadata_uri, {
        'from': _from, 
        'priority_fee': '10 wei',
        # "allow_revert": True
    })
    print('Token minted!')

# получение разрешения контракту передавать токен
# _from - владелец токена
# _to - лицо, которому даётся возможность управлять токеном
# token_id - id токена
def approve(_from, _to, token_id):
    PromissoryNFT[-1].approve(_to, token_id, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print('Approved!')

# Оплата векселя
# Требование:
# - _from == debtor 
def pay_promissory(promissory, _from, token_id):
    promissory.payPromissory({
        'from': _from,
        'value': '1100 wei',  
        'priority_fee': '10 wei'
    })
    PromissoryNFT[-1].burnCollectible(token_id, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    exist = PromissoryNFT[-1].existsCollectible(token_id, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    promissory.killContract({
        'from': _from,
        'priority_fee': '10 wei'
    })
    return exist

# Передача токена другому лицу (_to)
# Требование:
# - Разрешение распроряжаться токеном (approve) у передающего (owner)
# - Токен должен сущствовать
def transfer_token(owner, to, token_id):
    PromissoryNFT[-1].transferFrom(owner, to, token_id, {
        'from': owner,
        'priority_fee': '10 wei'
    })
    promissory = get_promissory(owner, token_id)
    promissory.setNewHolder(to, {
        'from': owner,
        'priority_fee': '10 wei'
    })
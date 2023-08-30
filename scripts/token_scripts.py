from brownie import PromissoryNFT, Promissory, accounts
from scripts.metadata import create_metadata

def main():
    holder = accounts.load('victor')
    debtor = accounts.load('victor2')
    deploy_promissory_nft(holder)
    create_promissory(holder, debtor, 10, 1000, 1691694000)

def deploy_promissory_nft(_from):
    promissory_nft_deployed = PromissoryNFT.deploy({
        "from": _from,
        'priority_fee': '2 gwei'
    })
    print(f"Promissory NFT deployed at {promissory_nft_deployed}")
    return promissory_nft_deployed

# Получение адреса контракта векселя по id, 
def get_promissory(_from, promissory_id):
    promissory = PromissoryNFT[-1].getPromissory(promissory_id, {
        'from': _from
    })
    return Promissory.at(promissory)

# Создание контракта, метаданных и выпуск токена
def create_promissory(_from, _debtor, _promissory_commission, _promissory_amount, _date_of_close):
    promissory_nft = PromissoryNFT[-1] 
    # проверяем количество отчеканенных на данный момент токенов
    existing_tokens = promissory_nft.tokenCounter()
    print(f'Existing tokens: {existing_tokens}')

    # вызываем нашу функцию createCollectible, чтобы создать контракт векселя 
    token_id = promissory_nft.createCollectible(_debtor, _promissory_commission, _promissory_amount, _date_of_close, {
        'from': _from,
        'priority_fee': '10 wei'
    }).return_value
    print('Create collectible!')

    # получаем хэш метаданных для URI этого токена
    metadata_uri = create_metadata(_from, token_id)
    print(f'Metadata URI: {metadata_uri}')

    # выпускаем токен
    promissory_nft.mintCollectible(metadata_uri, {
        'from': _from, 
        'priority_fee': '10 wei',
    })
    print('Token minted!')
    return token_id

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
from brownie import PromissoryNFT, accounts, config
from scripts.create_metadata import create_metadata

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

# Создание контракта, метаданных и выпуск токена
def create_promissory(_from, _debtor, _promissory_commission, _promissory_amount, _date_of_close):
    promissory_nft = PromissoryNFT[-1] 
    # проверяем количество отчеканенных на данный момент токенов
    existing_tokens = promissory_nft.tokenCounter()
    print(f'Existing tokens: {existing_tokens}')

    # вызываем нашу функцию createCollectible, чтобы создать контракт векселя 
    promissory_nft.createCollectible(_debtor, _promissory_commission, _promissory_amount, _date_of_close, {
        'from': _from,
        "gas_limit": 2074045
    })
    print('Create collectible!')

    # получаем хэш метаданных для URI этого токена
    metadata_uri = create_metadata(_from, existing_tokens+1)

    # выпускаем токен
    promissory_nft.mintCollectible(metadata_uri, {
        'from': _from, 
        'priority_fee': '10 wei',
        "allow_revert": True
    }).wait(3)
    print('Token minted!')

# получение разрешения контракту передавать токен
# _from - владелец токена
# _to - лицо, которому даётся возможность управлять токеном
# token_id - id токена
def approve(_from, _to, token_id):
    PromissoryNFT[-1].approve(_to, token_id, {
        'from': _from,
    })

# Получение адреса контракта векселя по id, преобразовывается в ContractContainer через Contract.at(address)
def get_promissory(_from, promissory_id):
    info = PromissoryNFT[-1].getPromissory(promissory_id, {
        'from': _from
    })
    return info
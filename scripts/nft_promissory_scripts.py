from brownie import PromissoryNFT, accounts, config
from scripts.create_metadata import create_metadata

def main():
    holder = accounts.load('victor')
    # deploy_promissory_nft(holder)
    create_promissory(holder, accounts.add(config['wallets']['debtor_key']), 0, 1000, 1691694000)

def deploy_promissory_nft(_from):
    promissoryNFT_deploy_contract = PromissoryNFT.deploy({
        "from": _from,
        'priority_fee': '2 gwei'
    })
    print(f"Promissory NFT deployed at {promissoryNFT_deploy_contract}")
    return promissoryNFT_deploy_contract

def create_promissory(_from, _debtor, _promissoryCommission, _promissoryAmount, _dateOfClose):
    promissory_collection = PromissoryNFT[-1] 
    # проверяем количество отчеканенных на данный момент токенов
    existing_tokens = promissory_collection.tokenCounter()
    print(f'Existing tokens: {existing_tokens}')

    # вызываем нашу функцию createCollectible, чтобы создать контракт sвекселя 
    promissory_collection.createCollectible(_debtor, _promissoryCommission, _promissoryAmount, _dateOfClose, {
        'from': _from,
        "gas_limit": 2074045,
        "allow_revert": True
    }).wait(1)
    print('Create collectible!')

    # получаем хэш метаданных для URI этого токена
    metadata_uri = create_metadata(_from)

    # выпускаем токен
    tx = promissory_collection.mintCollectible(metadata_uri, {
        'from': _from, 
        'priority_fee': '10 wei',
        "allow_revert": True
    })
    tx.wait(3)
    print('Token minted!')

def get_promissory(_from, promissory_id):
    info = PromissoryNFT[-1].getPromissory(promissory_id, {
        'from': _from
    })
    return info
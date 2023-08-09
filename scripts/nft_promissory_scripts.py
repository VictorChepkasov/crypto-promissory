from brownie import PromissoryNFT, accounts, config
import json
from pathlib import Path
from scripts.create_metadata import create_metadata

def main():
    holder = accounts.load('victor')
    deploy_promissory_nft(holder)
    create_promissory(holder, accounts.add(config['wallets']['debtor_key']), 0, 1000, 1691694000)

def deploy_promissory_nft(_from):
    promissoryNFT_deploy_contract = PromissoryNFT.deploy({
        "from": _from,
        'priority_fee': '2 gwei'
    }, publish_source=True)
    print(f"Promissory NFT deployed at {promissoryNFT_deploy_contract}")
    return promissoryNFT_deploy_contract

def create_promissory(_from, _debtor, _promissoryCommission, _promissoryAmount, _dateOfClose):
    promissory_collection = PromissoryNFT[-1]
    # проверяем количество отчеканенных на данный момент токенов
    existing_tokens = promissory_collection.tokenCounter()
    print(existing_tokens)

    # вызываем нашу функцию createCollectible, чтобы создать контракт
    promissory_collection.createCollectible(_debtor, _promissoryCommission, _promissoryAmount, _dateOfClose, {
        'from': _from, 
        "gas_limit": 2074045,
        "allow_revert": True
    }).wait(1)

    # получаем хэш метаданных для URI этого токена
    metadata_hash = create_metadata(_from)

    # выпускаем токен
    transaction = promissory_collection.mintCollectible(metadata_hash, {
        'from': _from, 
        'priority_fee': '3 gwei',
        "allow_revert": True
    })
    transaction.wait(3)
    print('Token minted!')


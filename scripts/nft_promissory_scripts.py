from brownie import PromissoryNFT, accounts, config
import json
from pathlib import Path
from scripts.create_metadata import create_metadata

def main():
    holder = accounts.load('victor')
    # deploy_promissory_nft(holder)
    mint_promissry(holder)

def deploy_promissory_nft(_from):
    promissoryNFT_deploy_contract = PromissoryNFT.deploy({
        "from": _from,
        'priority_fee': '3 gwei'
    }, publish_source=True)
    print(f"Promissory NFT deployed at {promissoryNFT_deploy_contract}")
    return promissoryNFT_deploy_contract

def mint_promissry(_from):
    promissory_collection = PromissoryNFT[-1]
    # проверяем количество отчеканенных на данный момент токенов
    existing_tokens = promissory_collection.tokenCounter()
    print(existing_tokens)

    # проверяем, готовы ли уже хэши метаданных
    if Path(f"./scripts/metadata/metadata_hashes.json").exists():
        print("Metadata already exists. Skipping...")
        metadata_hashes = json.load(open(f"./scripts/metadata/metadata_hashes.json"))
    else:
        metadata_hashes = create_metadata(1)

    for token_id in range(existing_tokens, 1):
        # получаем хэш метаданных для URI этого токена
        metadata_hash = metadata_hashes[token_id]
        # вызываем нашу функцию createCollectible, чтобы создать токен
        transaction = promissory_collection.createCollectible(metadata_hash, {
            'from': _from, 
            "gas_limit": 2074045,
            "allow_revert": True
        })
    
    transaction.wait(3)


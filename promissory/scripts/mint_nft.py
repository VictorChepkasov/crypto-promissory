import json
from pathlib import Path
from brownie import (
    accounts,
    PromissoryNFT,
)
from scripts.create_metadata import create_metadata



def main():
    mint_promissry()

def mint_promissry():
    holder = accounts.load('victor')
    promissory_collection = PromissoryNFT[-1]
    existing_tokens = promissory_collection.tokenCounter()

    if Path(f"./scripts/metadata/data.json").exists():
        print("Metadata already exists. Skipping...")
        metadata_hashes = json.load(open(f"./scripts/metadata/data.json"))
    else:
        metadata_hashes = create_metadata(1)

    for token_id in range(existing_tokens, 1):
        metadata_hash = metadata_hashes[token_id]

        transaction = promissory_collection.createCollectible(metadata_hash, {'from': holder,  "gas_limit": 2074045, "allow_revert": True})
    
    transaction.wait(3)
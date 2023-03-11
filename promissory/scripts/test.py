import json
from pathlib import Path
from brownie import (
    accounts,
    config,
    WaterCollection,
)
from scripts.WaterCollection.create_metadata import write_metadata

def main():
    # Get our account info
    dev = accounts.add(config['wallets']['from_key'])
		# Get the most recent deployment of our contract
    water_collection = WaterCollection[-1]
		# Check the number of currently minted tokens
    existing_tokens = water_collection.tokenCounter()
    print(existing_tokens)
    # Check if we'eve already got our metadata hashes ready
    if Path(f"metadata/data.json").exists():
        print("Metadata already exists. Skipping...")
        meta_data_hashes = json.load(open(f"metadata/data.json"))
    else:
        meta_data_hashes = write_metadata(100)
    for token_id in range(existing_tokens, 100):
        # Get the metadata hash for this token's URI
        meta_data_hash = meta_data_hashes[token_id]
        # Call our createCollectible function to mint a token
        transaction = water_collection.createCollectible(
            meta_data_hash, {'from': dev,  "gas_limit": 2074044, "allow_revert": True})
    # Wait for 3 blocks to be created atop our transactions
    transaction.wait(3)
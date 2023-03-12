import json
from pathlib import Path
from brownie import (
    accounts,
    config,
    WaterCollection,
)
from scripts.WaterCollection.create_metadata import write_metadata

def main():
    # получаем информацию о нашей учетной записи
    dev = accounts.add(config['wallets']['from_key'])
		# получаем самое последнее развертывание нашего контракта
    water_collection = WaterCollection[-1]
		# проверяем количество отчеканенных на данный момент токенов
    existing_tokens = water_collection.tokenCounter()
    print(existing_tokens)
    # проверяем, готовы ли уже хэши метаданных
    if Path(f"metadata/data.json").exists():
        print("Metadata already exists. Skipping...")
        meta_data_hashes = json.load(open(f"metadata/data.json"))
    else:
        meta_data_hashes = write_metadata(100)
    for token_id in range(existing_tokens, 100):
        # получаем хэш метаданных для URI этого токена
        meta_data_hash = meta_data_hashes[token_id]
        # вызываем нашу функцию createCollectible, чтобы создать токен
        transaction = water_collection.createCollectible(
            meta_data_hash, {'from': dev,  "gas_limit": 2074044, "allow_revert": True})
    # ждём, пока будут созданы 3 блока поверх наших транзакций.
    transaction.wait(3)
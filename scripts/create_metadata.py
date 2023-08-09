import requests
import os
import json
from brownie import Promissory, PromissoryNFT, accounts, config
from dotenv import load_dotenv
from scripts.promissory_scripts import get_promissory_info

load_dotenv()

metadata_template = {
    "name": "",
    "attributes": [
        {
            "trait_type": "holder address",
            "value": ""
        },
        {
            "trait_type": "debtor address",
            "value": ""
        },
        {
            "trait_type": "commission in percents",
            "value": ""
        },
        {
            "trait_type": "amount",
            "value": ""
        },
        {
            "trait_type": "date of registration",
            "value": ""
        },
        {
            "trait_type": "date of close",
            "value": ""
        },
        {
            "trait_type": "date of holder consent",
            "value": ""
        },
        {
            "trait_type": "date of debtor consent",
            "value": ""
        },
        {
            "trait_type": "holder consent",
            "value": ""
        },
        {
            "trait_type": "debtor consent",
            "value": ""
        }
        ]
    }

def main():
    create_metadata(3, accounts.add(config["wallets"]['from_key']))

def create_metadata(i, _from):
    # разворачиваем контракт и получаем инфу о нём
    promissory_info = get_promissory_info_arr(_from)
    # массив для хранения метаданных
    metadata_hashes = []

    existing_tokens = PromissoryNFT[-1].tokenCounter()
    print(existing_tokens)

    for token_id in range(existing_tokens, i):
        # копируем шаблон метаданных
        collectible_metadata = metadata_template.copy()
        # имя файла метаданных
        metadata_filename = f"./scripts/metadata/tokens/{token_id+1}.json"
        # имя токена = его id
        collectible_metadata["name"] = str(token_id+1)

        # сохраняем данные контракта в виде атрибутов
        for index in range(10):
            metadata_template["attributes"][index]["value"] = str(promissory_info[index])

        with open(metadata_filename, "w") as f:
            # Запишите метаданные локально
            json.dump(collectible_metadata, f)

        # загрузка данных в ipfs(Pinata)
        metadata_hash = upload_to_ipfs(collectible_metadata)
        metadata_path = f"<https://ipfs.io/ipfs/{metadata_hash}>"
 
        # добавить uri метаданных в массив
        metadata_hashes.append(metadata_path)
    
    with open('./scripts/metadata/metadata_hashes.json', 'w') as f:
        # запись массива URI метаданных в файл
        json.dump(metadata_hashes, f)
 
    print('Metadata created success!')
    return metadata_hashes

def upload_to_ipfs(data):
    endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    # на случай, если понадобится работа JWT. В прошлый раз так всё работало
    # pinata_api_jwt = os.environ.get("PINATA_API_JWT")
    # headers = {
        # 'Authorization': pinata_api_jwt,
    # }
    pinata_api_key = os.environ.get("PINATA_API_KEY")
    pinata_secret_api_key = os.environ.get("PINATA_API_SECRET")
    headers = {
        'pinata_api_key': pinata_api_key,
        'pinata_secret_api_key': pinata_secret_api_key
    }
    encode_data = json.dumps(data, indent=2).encode('utf-8')
    print(f"Data for encode: {data}")
    files = {
        'file': encode_data
    }

    # запрос пин-кода в pinata
    response = requests.post(endpoint, headers=headers, files=files)
    print(f'Response: {response.json()}')
    returned_hash_IPFS = response.json()['IpfsHash']
    print(f"""
          Response: {response.json()}
          Returned value: {returned_hash_IPFS}
          """)
    
    # возвращаем хэш ipfs, где хранятся все нужные данные
    return returned_hash_IPFS

def get_promissory_info_arr(_from):
    promissory_info = get_promissory_info(_from)
    #clean promissory info
    chars = "()''"
    promissory_info = str(promissory_info).translate(str.maketrans('', '', chars)).split(', ')
    return promissory_info